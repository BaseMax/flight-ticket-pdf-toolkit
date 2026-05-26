"""
Flight ticket PDF modifier.

Edit the CONFIG section at the bottom of this file, then run:
    python generate.py

Core fixes vs. original:
  - apply_redactions() is now called ONCE per page after all annotations
    are added (not inside the per-rect loop — that corrupted page state)
  - PyMuPDF color integers are unpacked to (r, g, b) float tuples
  - Text insertion shrinks font size when rect is too small
  - Replacements are sorted longest-key-first to prevent short tokens
    (e.g. "IST") from matching inside longer strings ("Istanbul")
"""
from __future__ import annotations

import random
import string
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import NamedTuple
from zoneinfo import ZoneInfo

import fitz  # PyMuPDF


# ═══════════════════════════════════════════════════════════ Types ═══════════


@dataclass(frozen=True)
class Airport:
    city: str
    name: str
    iata: str
    country: str
    timezone: str


@dataclass
class Config:
    input_file: Path
    output_file: Path

    # ── What is currently in the PDF (searched and erased) ───────────────────
    src_departure: Airport
    src_departure_date: str    # "27 May 2026"
    src_departure_time: str    # "10:45"
    src_arrival: Airport
    src_arrival_time: str      # "14:15"
    src_airline: str           # airline name as it appears in the PDF
    src_pnr: str               # booking reference as it appears in the PDF

    # ── What to write in its place ───────────────────────────────────────────
    dst_departure: Airport
    dst_departure_datetime: str  # "27 May 2026 10:45"
    dst_arrival: Airport
    flight_duration: str          # "HH:MM"  — used to compute arrival time
    dst_airline: str
    dst_pnr: str

    name_replacements: dict[str, str] = field(default_factory=dict)
    extra_replacements: dict[str, str] = field(default_factory=dict)
    logo_path: Path | None = None  # replace largest image on each page with this


class _Style(NamedTuple):
    font: str
    size: float
    color: int  # packed sRGB integer (PyMuPDF native format)


# ══════════════════════════════════════════════════════ PDF internals ════════

# Prevent image content from being erased when applying text-only redactions.
_REDACT_TEXT_ONLY: int = getattr(fitz, "PDF_REDACT_IMAGE_NONE", 0)


def _unpack_rgb(c: int) -> tuple[float, float, float]:
    return ((c >> 16) & 0xFF) / 255.0, ((c >> 8) & 0xFF) / 255.0, (c & 0xFF) / 255.0


def _style_at(page: fitz.Page, rect: fitz.Rect) -> _Style:
    """Return the font/size/color of the first span that intersects rect."""
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                if rect.intersects(fitz.Rect(span["bbox"])):
                    return _Style(
                        font=str(span.get("font", "helv")),
                        size=float(span.get("size", 10)),
                        color=int(span.get("color", 0)),
                    )
    return _Style("helv", 10.0, 0)


def _pick_font(font_name: str) -> str:
    """Return the closest built-in PDF font for the given embedded font name."""
    n = font_name.lower()
    bold   = "bold" in n or "black" in n or "heavy" in n
    italic = "italic" in n or "oblique" in n
    if bold and italic:
        return "hebi"
    if bold:
        return "hebo"
    if italic:
        return "heit"
    return "helv"


def _write_into(page: fitz.Page, rect: fitz.Rect, text: str, style: _Style) -> None:
    """Insert text into rect, shrinking font size if it does not fit."""
    color = _unpack_rgb(style.color)
    font  = _pick_font(style.font)
    for size in (style.size, style.size * 0.85, max(6.0, style.size * 0.70)):
        if page.insert_textbox(rect, text, fontsize=size, fontname=font,
                               color=color, align=0) >= 0:
            return
    # Absolute fallback: free-positioned text anchored at the left baseline.
    page.insert_text(
        (rect.x0, rect.y1 - 1), text,
        fontsize=max(6.0, style.size * 0.70), fontname=font, color=color,
    )


def apply_replacements(page: fitz.Page, replacements: dict[str, str]) -> None:
    """
    Erase every occurrence of each key on the page and write the value.

    All redact annotations are added first, then applied in one shot — this
    is the critical fix. The original code called apply_redactions() inside
    the loop, which invalidated subsequent search results on the same page.

    Keys are processed longest-first so that multi-word strings (e.g.
    "Istanbul Airport") are handled before their substrings ("Istanbul").
    """
    pairs = sorted(
        [(k, v) for k, v in replacements.items() if k and k != v],
        key=lambda t: len(t[0]),
        reverse=True,
    )

    # Phase 1 — collect rects and record styles before any redaction
    pending: list[tuple[fitz.Rect, str, _Style]] = []
    for old, new in pairs:
        for rect in page.search_for(old):
            pending.append((rect, new, _style_at(page, rect)))
            page.add_redact_annot(rect, fill=(1, 1, 1))

    if not pending:
        return

    # Phase 2 — single apply call (the fix)
    page.apply_redactions(images=_REDACT_TEXT_ONLY)

    # Phase 3 — insert replacement text
    for rect, text, style in pending:
        _write_into(page, rect, text, style)


def replace_logo(page: fitz.Page, logo: Path) -> None:
    """Swap the largest image on the page with the given logo file."""
    best_rect, best_area = fitz.Rect(), 0.0
    for info in page.get_image_info():
        if bbox := info.get("bbox"):
            rect = fitz.Rect(bbox)
            if (area := rect.get_area()) > best_area:
                best_rect, best_area = rect, area
    if best_area == 0.0:
        return
    page.add_redact_annot(best_rect, fill=(1, 1, 1))
    page.apply_redactions()
    page.insert_image(best_rect, filename=str(logo), keep_proportion=True)


# ════════════════════════════════════════════════════════ Time helpers ════════


def _parse_hhmm(s: str) -> timedelta:
    h, m = map(int, s.split(":"))
    return timedelta(hours=h, minutes=m)


def compute_times(cfg: Config) -> tuple[datetime, datetime]:
    """Return (departure_dt, arrival_dt) in their respective local timezones."""
    dep = datetime.strptime(cfg.dst_departure_datetime, "%d %b %Y %H:%M").replace(
        tzinfo=ZoneInfo(cfg.dst_departure.timezone)
    )
    arr = (dep + _parse_hhmm(cfg.flight_duration)).astimezone(
        ZoneInfo(cfg.dst_arrival.timezone)
    )
    return dep, arr


# ════════════════════════════════════════════════════ Booking reference ═══════


def random_booking_ref(length: int = 6) -> str:
    """Return a random uppercase alphanumeric booking reference."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


# ══════════════════════════════════════════════════════════════ Core ══════════


def _build_replacements(cfg: Config, dep: datetime, arr: datetime) -> dict[str, str]:
    s, d = cfg.src_departure, cfg.dst_departure
    sa, da = cfg.src_arrival, cfg.dst_arrival
    return {
        **cfg.name_replacements,
        **cfg.extra_replacements,
        cfg.src_airline: cfg.dst_airline,
        cfg.src_pnr: cfg.dst_pnr,
        # Airport full names (longer — handled before cities/IATA by sort)
        s.name:    d.name,
        sa.name:   da.name,
        s.city:    d.city,
        sa.city:   da.city,
        s.country: d.country,
        sa.country: da.country,
        s.iata:    d.iata,
        sa.iata:   da.iata,
        # Date / time
        cfg.src_departure_date: dep.strftime("%d %b %Y"),
        cfg.src_departure_time: dep.strftime("%H:%M"),
        cfg.src_arrival_time:   arr.strftime("%H:%M"),
    }


def process(cfg: Config) -> None:
    dep, arr = compute_times(cfg)
    replacements = _build_replacements(cfg, dep, arr)

    doc = fitz.open(cfg.input_file)
    for page in doc:
        apply_replacements(page, replacements)
        if cfg.logo_path and cfg.logo_path.exists():
            replace_logo(page, cfg.logo_path)

    doc.save(cfg.output_file)
    doc.close()
    print(f"Saved -> {cfg.output_file}")


# ═══════════════════════════════════════════════════════════ Config ═══════════

if __name__ == "__main__":
    # ── Source airports: exactly as the text appears in the input PDF ─────────
    IST = Airport(
        city="Istanbul",
        name="Istanbul Airport",
        iata="IST",
        country="Turkey",
        timezone="Europe/Istanbul",
    )
    IKA = Airport(
        city="Tehran",
        name="Imam Khomeini Intl",
        iata="IKA",
        country="Iran",
        timezone="Asia/Tehran",
    )

    # ── To reroute, swap dst_departure / dst_arrival for different Airport
    #    objects. To keep the same route, leave them identical to src_*.  ─────
    cfg = Config(
        input_file=Path("input.pdf"),
        output_file=Path("output.pdf"),

        # Current PDF content ─────────────────────────────────────────────────
        src_departure=IST,
        src_departure_date="27 May 2026",
        src_departure_time="10:45",
        src_arrival=IKA,
        src_arrival_time="14:15",
        src_airline="Mahan Air",
        src_pnr="ABC123",

        # Replacement content ─────────────────────────────────────────────────
        dst_departure=IST,
        dst_departure_datetime="27 May 2026 10:45",
        dst_arrival=IKA,
        flight_duration="03:00",
        dst_airline="Mahan Air",
        dst_pnr=random_booking_ref(),  # or hardcode: "XYZ789"

        name_replacements={
            # Replace the full name as one unit so the lname position
            # follows the rendered width of the fname rather than the
            # fixed position of the original lname span.
            "MR SEYYEDALI MOHAMMADIYEH": "MR MOHAMMADALI RAHIMI",
        },

        # Uncomment to swap the airline logo (supply your own image):
        # logo_path=Path("logo.png"),
    )

    process(cfg)
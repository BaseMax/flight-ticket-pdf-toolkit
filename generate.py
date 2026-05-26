import fitz # PyMuPDF
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

INPUT_FILE = "input.pdf"
OUTPUT_FILE = "output.pdf"

# ---------------- CONFIG ---------------- #
FLIGHT_DURATION = "03:00"  # HH:MM

DEPARTURE = {
    "city": "Istanbul",
    "airport": "Istanbul Airport",
    "iata": "IST",
    "country": "Turkey",
    "datetime": "27 May 2026 10:45",
    "timezone": "Europe/Istanbul"
}

ARRIVAL = {
    "city": "Tehran",
    "airport": "Imam Khomeini Intl",
    "iata": "IKA",
    "country": "Iran",
    "timezone": "Asia/Tehran"
}

NAME_REPLACEMENTS = {
    "SEYYEDALI": "MOHAMMADALI",
    "MOHAMMADIYEH": "RAHIMI"
}


def parse_duration(duration_str):
    h, m = map(int, duration_str.split(":"))
    return timedelta(hours=h, minutes=m)


def compute_arrival():
    dep_dt = datetime.strptime(DEPARTURE["datetime"], "%d %b %Y %H:%M")
    dep_dt = dep_dt.replace(tzinfo=ZoneInfo(DEPARTURE["timezone"]))

    duration = parse_duration(FLIGHT_DURATION)

    arr_dt = dep_dt + duration
    arr_dt = arr_dt.astimezone(ZoneInfo(ARRIVAL["timezone"]))

    return dep_dt, arr_dt


def format_date(dt):
    return dt.strftime("%d %b %Y")


def format_time(dt):
    return dt.strftime("%H:%M")


def get_text_style(page, rect):
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                span_rect = fitz.Rect(span["bbox"])
                if rect.intersects(span_rect):
                    return {
                        "font": span.get("font", "helv"),
                        "size": span.get("size", 10),
                        "color": span.get("color", 0)
                    }

    return {"font": "helv", "size": 10, "color": 0}


def replace_text(page, old, new):
    areas = page.search_for(old)

    for rect in areas:
        style = get_text_style(page, rect)

        page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()

        page.insert_textbox(
            rect,
            new,
            fontsize=style["size"],
            fontname="helv",
            color=(0, 0, 0),
            align=0
        )


def process_pdf(input_path, output_path):
    doc = fitz.open(input_path)

    dep_dt, arr_dt = compute_arrival()

    replacements = {
        **NAME_REPLACEMENTS,

        "Istanbul": DEPARTURE["city"],
        "Turkey": DEPARTURE["country"],
        "IST": DEPARTURE["iata"],
        "Istanbul Airport": DEPARTURE["airport"],

        "Tehran": ARRIVAL["city"],
        "Iran": ARRIVAL["country"],
        "IKA": ARRIVAL["iata"],
        "Imam Khomeini Intl": ARRIVAL["airport"],

        "27 May 2026": format_date(dep_dt),
        "10:45": format_time(dep_dt),
        "14:15": format_time(arr_dt),
    }

    arrival_date_str = format_date(arr_dt)

    replacements["27 May 2026"] = format_date(dep_dt)

    for page in doc:
        for old, new in replacements.items():
            replace_text(page, old, new)

        replace_text(page, "27 May 2026", arrival_date_str)

    doc.save(output_path)
    doc.close()


if __name__ == "__main__":
    process_pdf(INPUT_FILE, OUTPUT_FILE)
    print("✅ Done ->", OUTPUT_FILE)

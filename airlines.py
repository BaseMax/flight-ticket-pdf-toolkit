"""
Airlines database — IATA / ICAO codes for major world carriers.

Usage:
    from airlines import find_airline, airlines_by_country, AIRLINES
    a = find_airline("Mahan Air")   # by name, IATA, or ICAO
    iranian = airlines_by_country("Iran")
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Airline:
    name: str
    iata: str   # 2-letter IATA designator
    icao: str   # 3-letter ICAO designator
    country: str
    hub: str    # primary hub (IATA airport code)


# ─────────────────────────────────────────────────────────── Iranian ──────────

IRAN: tuple[Airline, ...] = (
    Airline("Iran Air",               "IR",  "IRA",  "Iran",  "IKA"),
    Airline("Mahan Air",              "W5",  "IRM",  "Iran",  "IKA"),
    Airline("Iran Aseman Airlines",   "EP",  "IRC",  "Iran",  "IKA"),
    Airline("Qeshm Air",              "QB",  "QSM",  "Iran",  "GSM"),
    Airline("Caspian Airlines",       "RV",  "CPN",  "Iran",  "IKA"),
    Airline("Zagros Airlines",        "Z4",  "IZG",  "Iran",  "IKA"),
    Airline("Kish Air",               "Y9",  "KIS",  "Iran",  "KIH"),
    Airline("Sepehran Airlines",      "IS",  "SHI",  "Iran",  "IKA"),
    Airline("Taban Air",              "HH",  "TBN",  "Iran",  "MHD"),
    Airline("Meraj Airlines",         "MJ",  "MRJ",  "Iran",  "IKA"),
    Airline("Pouya Air",              "PY",  "PYA",  "Iran",  "IKA"),
    Airline("Saha Airlines",          "IRZ", "IRZ",  "Iran",  "IKA"),
    Airline("Varesh Airlines",        "VR",  "VRH",  "Iran",  "MHD"),
    Airline("Fly Persian",            "7P",  "FPS",  "Iran",  "IKA"),
    Airline("Iranian Naft Airlines",  "I4",  "IRG",  "Iran",  "AHW"),
)

# ─────────────────────────────────────────────────────────── European ─────────

EUROPE: tuple[Airline, ...] = (
    # Full-service
    Airline("Lufthansa",              "LH",  "DLH",  "Germany",      "FRA"),
    Airline("British Airways",        "BA",  "BAW",  "UK",           "LHR"),
    Airline("Air France",             "AF",  "AFR",  "France",       "CDG"),
    Airline("KLM",                    "KL",  "KLM",  "Netherlands",  "AMS"),
    Airline("Swiss",                  "LX",  "SWR",  "Switzerland",  "ZRH"),
    Airline("Austrian Airlines",      "OS",  "AUA",  "Austria",      "VIE"),
    Airline("Brussels Airlines",      "SN",  "BEL",  "Belgium",      "BRU"),
    Airline("Finnair",                "AY",  "FIN",  "Finland",      "HEL"),
    Airline("SAS Scandinavian",       "SK",  "SAS",  "Sweden",       "CPH"),
    Airline("Iberia",                 "IB",  "IBE",  "Spain",        "MAD"),
    Airline("TAP Air Portugal",       "TP",  "TAP",  "Portugal",     "LIS"),
    Airline("Aer Lingus",             "EI",  "EIN",  "Ireland",      "DUB"),
    Airline("Turkish Airlines",       "TK",  "THY",  "Turkey",       "IST"),
    Airline("ITA Airways",            "AZ",  "ITY",  "Italy",        "FCO"),
    Airline("LOT Polish Airlines",    "LO",  "LOT",  "Poland",       "WAW"),
    Airline("Czech Airlines",         "OK",  "CSA",  "Czech Rep.",   "PRG"),
    Airline("Aegean Airlines",        "A3",  "AEE",  "Greece",       "ATH"),
    Airline("Croatia Airlines",       "OU",  "CTN",  "Croatia",      "ZAG"),
    Airline("Air Serbia",             "JU",  "ASL",  "Serbia",       "BEG"),
    Airline("TAROM",                  "RO",  "ROT",  "Romania",      "OTP"),
    Airline("Bulgaria Air",           "FB",  "LZB",  "Bulgaria",     "SOF"),
    Airline("Air Malta",              "KM",  "AMC",  "Malta",        "MLA"),
    Airline("Luxair",                 "LG",  "LGL",  "Luxembourg",   "LUX"),
    Airline("Air Baltic",             "BT",  "BTI",  "Latvia",       "RIX"),
    Airline("Aeroflot",               "SU",  "AFL",  "Russia",       "SVO"),
    Airline("S7 Airlines",            "S7",  "SBI",  "Russia",       "DME"),
    Airline("Ural Airlines",          "U6",  "SVR",  "Russia",       "SVX"),
    Airline("UTair",                  "UT",  "UTA",  "Russia",       "SVO"),
    # Low-cost
    Airline("Ryanair",                "FR",  "RYR",  "Ireland",      "DUB"),
    Airline("easyJet",                "U2",  "EZY",  "UK",           "LGW"),
    Airline("Wizz Air",               "W6",  "WZZ",  "Hungary",      "BUD"),
    Airline("Vueling",                "VY",  "VLG",  "Spain",        "BCN"),
    Airline("Norwegian",              "DY",  "NAX",  "Norway",       "OSL"),
    Airline("Transavia",              "HV",  "TRA",  "Netherlands",  "AMS"),
    Airline("Transavia France",       "TO",  "TVF",  "France",       "ORY"),
    Airline("Pegasus Airlines",       "PC",  "PGT",  "Turkey",       "SAW"),
    Airline("SunExpress",             "XQ",  "SXS",  "Turkey",       "AYT"),
    Airline("Volotea",                "V7",  "VOE",  "Spain",        "BCN"),
    Airline("Wideroe",                "WF",  "WIF",  "Norway",       "BGO"),
)

# ────────────────────────────────────────────────────────── Middle East ───────

MIDDLE_EAST: tuple[Airline, ...] = (
    Airline("Emirates",               "EK",  "UAE",  "UAE",           "DXB"),
    Airline("Etihad Airways",         "EY",  "ETD",  "UAE",           "AUH"),
    Airline("Qatar Airways",          "QR",  "QTR",  "Qatar",         "DOH"),
    Airline("flydubai",               "FZ",  "FDB",  "UAE",           "DXB"),
    Airline("Air Arabia",             "G9",  "ABY",  "UAE",           "SHJ"),
    Airline("Gulf Air",               "GF",  "GFA",  "Bahrain",       "BAH"),
    Airline("Kuwait Airways",         "KU",  "KAC",  "Kuwait",        "KWI"),
    Airline("Royal Jordanian",        "RJ",  "RJA",  "Jordan",        "AMM"),
    Airline("Middle East Airlines",   "ME",  "MEA",  "Lebanon",       "BEY"),
    Airline("flynas",                 "XY",  "KNE",  "Saudi Arabia",  "RUH"),
    Airline("Saudia",                 "SV",  "SVA",  "Saudi Arabia",  "JED"),
    Airline("Flyadeal",               "F3",  "FAD",  "Saudi Arabia",  "JED"),
    Airline("Oman Air",               "WY",  "OMA",  "Oman",          "MCT"),
    Airline("Iraqi Airways",          "IA",  "IAW",  "Iraq",          "BGW"),
    Airline("Air Arabia Abu Dhabi",   "3L",  "ADA",  "UAE",           "AUH"),
    Airline("SalamAir",               "OV",  "OMS",  "Oman",          "MCT"),
)

# ────────────────────────────────────────────────────────────── Asia ──────────

ASIA: tuple[Airline, ...] = (
    Airline("Japan Airlines",         "JL",  "JAL",  "Japan",        "NRT"),
    Airline("All Nippon Airways",     "NH",  "ANA",  "Japan",        "HND"),
    Airline("Singapore Airlines",     "SQ",  "SIA",  "Singapore",    "SIN"),
    Airline("Scoot",                  "TR",  "TGW",  "Singapore",    "SIN"),
    Airline("Cathay Pacific",         "CX",  "CPA",  "Hong Kong",    "HKG"),
    Airline("Korean Air",             "KE",  "KAL",  "South Korea",  "ICN"),
    Airline("Asiana Airlines",        "OZ",  "AAR",  "South Korea",  "ICN"),
    Airline("Air China",              "CA",  "CCA",  "China",        "PEK"),
    Airline("China Eastern",          "MU",  "CES",  "China",        "PVG"),
    Airline("China Southern",         "CZ",  "CSN",  "China",        "CAN"),
    Airline("Hainan Airlines",        "HU",  "CHH",  "China",        "PEK"),
    Airline("Xiamen Air",             "MF",  "CXA",  "China",        "XMN"),
    Airline("Thai Airways",           "TG",  "THA",  "Thailand",     "BKK"),
    Airline("Bangkok Airways",        "PG",  "BKP",  "Thailand",     "BKK"),
    Airline("Malaysia Airlines",      "MH",  "MAS",  "Malaysia",     "KUL"),
    Airline("AirAsia",                "AK",  "AXM",  "Malaysia",     "KUL"),
    Airline("Garuda Indonesia",       "GA",  "GIA",  "Indonesia",    "CGK"),
    Airline("Lion Air",               "JT",  "LNI",  "Indonesia",    "CGK"),
    Airline("Philippine Airlines",    "PR",  "PAL",  "Philippines",  "MNL"),
    Airline("Cebu Pacific",           "5J",  "CEB",  "Philippines",  "MNL"),
    Airline("Vietnam Airlines",       "VN",  "HVN",  "Vietnam",      "HAN"),
    Airline("Vietjet Air",            "VJ",  "VJC",  "Vietnam",      "SGN"),
    Airline("Air India",              "AI",  "AIC",  "India",        "DEL"),
    Airline("IndiGo",                 "6E",  "IGO",  "India",        "DEL"),
    Airline("SpiceJet",               "SG",  "SEJ",  "India",        "DEL"),
    Airline("SriLankan Airlines",     "UL",  "ALK",  "Sri Lanka",    "CMB"),
    Airline("Pakistan International", "PK",  "PIA",  "Pakistan",     "KHI"),
)

# ────────────────────────────────────────────────────────────── Africa ────────

AFRICA: tuple[Airline, ...] = (
    Airline("Ethiopian Airlines",     "ET",  "ETH",  "Ethiopia",     "ADD"),
    Airline("Kenya Airways",          "KQ",  "KQA",  "Kenya",        "NBO"),
    Airline("South African Airways",  "SA",  "SAA",  "South Africa", "JNB"),
    Airline("EgyptAir",               "MS",  "MSR",  "Egypt",        "CAI"),
    Airline("Royal Air Maroc",        "AT",  "RAM",  "Morocco",      "CMN"),
    Airline("Air Mauritius",          "MK",  "MAU",  "Mauritius",    "MRU"),
    Airline("Tunisair",               "TU",  "TAR",  "Tunisia",      "TUN"),
    Airline("Air Algerie",            "AH",  "DAH",  "Algeria",      "ALG"),
    Airline("ASKY Airlines",          "KP",  "SKY",  "Togo",         "LFW"),
    Airline("Afriqiyah Airways",      "8U",  "AAW",  "Libya",        "TIP"),
)

# ──────────────────────────────────────────────────────────── Americas ────────

AMERICAS: tuple[Airline, ...] = (
    Airline("American Airlines",      "AA",  "AAL",  "USA",       "DFW"),
    Airline("Delta Air Lines",        "DL",  "DAL",  "USA",       "ATL"),
    Airline("United Airlines",        "UA",  "UAL",  "USA",       "ORD"),
    Airline("Southwest Airlines",     "WN",  "SWA",  "USA",       "DAL"),
    Airline("JetBlue Airways",        "B6",  "JBU",  "USA",       "JFK"),
    Airline("Alaska Airlines",        "AS",  "ASA",  "USA",       "SEA"),
    Airline("Spirit Airlines",        "NK",  "NKS",  "USA",       "FLL"),
    Airline("Frontier Airlines",      "F9",  "FFT",  "USA",       "DEN"),
    Airline("Air Canada",             "AC",  "ACA",  "Canada",    "YYZ"),
    Airline("WestJet",                "WS",  "WJA",  "Canada",    "YYC"),
    Airline("Aeromexico",             "AM",  "AMX",  "Mexico",    "MEX"),
    Airline("Volaris",                "Y4",  "VOI",  "Mexico",    "MEX"),
    Airline("LATAM Airlines",         "LA",  "LAN",  "Chile",     "SCL"),
    Airline("GOL Airlines",           "G3",  "GLO",  "Brazil",    "GRU"),
    Airline("Avianca",                "AV",  "AVA",  "Colombia",  "BOG"),
    Airline("Copa Airlines",          "CM",  "CMP",  "Panama",    "PTY"),
    Airline("Caribbean Airlines",     "BW",  "BWA",  "Trinidad",  "POS"),
)

# ──────────────────────────────────────────────────────────── Oceania ─────────

OCEANIA: tuple[Airline, ...] = (
    Airline("Qantas",                 "QF",  "QFA",  "Australia",   "SYD"),
    Airline("Jetstar",                "JQ",  "JST",  "Australia",   "SYD"),
    Airline("Virgin Australia",       "VA",  "VOZ",  "Australia",   "BNE"),
    Airline("Air New Zealand",        "NZ",  "ANZ",  "New Zealand", "AKL"),
    Airline("Fiji Airways",           "FJ",  "FJI",  "Fiji",        "NAN"),
)

# ─────────────────────────────────────────────────────────── Combined ─────────

AIRLINES: tuple[Airline, ...] = (
    *IRAN, *EUROPE, *MIDDLE_EAST, *ASIA, *AFRICA, *AMERICAS, *OCEANIA
)

# ─────────────────────────────────────────────────────────── Lookups ──────────


def find_airline(query: str) -> Airline | None:
    """Look up by exact name, IATA code, or ICAO code (case-insensitive), then partial name."""
    q = query.strip().lower()
    for a in AIRLINES:
        if q in (a.iata.lower(), a.icao.lower(), a.name.lower()):
            return a
    for a in AIRLINES:
        if q in a.name.lower():
            return a
    return None


def airlines_by_country(country: str) -> list[Airline]:
    """Return all airlines whose country contains the given string (case-insensitive)."""
    c = country.strip().lower()
    return [a for a in AIRLINES if c in a.country.lower()]
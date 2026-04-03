"""
Configuration for the Job Alert Agent.
Edit these values to customize your job search.
"""

# ─── Job Search Settings ───────────────────────────────────────────────

SEARCH_QUERIES = [
    "Recruiting Manager",
    "Senior Recruiting Manager",
    "Talent Acquisition Manager",
    "Senior Talent Acquisition Manager",
    "Talent Manager",
    "Director Talent Acquisition",
    "Recruiting Director",
]

LOCATIONS = [
    "San Francisco Bay Area, CA",
    "Remote",
]

# Job boards to scrape: "linkedin", "indeed", "google"
# Google Jobs can be rate-limited from some IPs. Enable it on GitHub Actions.
# To enable: add "google" to the list below
SITES = ["linkedin", "indeed"]

# Only fetch jobs posted within this many hours
# 2-hour lookback gives safety margin for the 30-min check cycle
HOURS_OLD = 2

# Max results per search query per site
RESULTS_WANTED = 25

# Country for Indeed filtering
COUNTRY_INDEED = "USA"

# ─── Relevance Filtering ─────────────────────────────────────────────

# Job title MUST contain at least one of these keywords (case-insensitive)
# to be considered relevant
TITLE_MUST_CONTAIN = [
    "recruit",
    "talent acquisition",
    "talent manager",
    "talent management",
    "ta manager",
    "ta director",
    "hiring manager",
    "staffing manager",
    "staffing director",
    "people acquisition",
]

# Job titles containing any of these keywords will be EXCLUDED
TITLE_EXCLUDE = [
    "intern",
    "coordinator",
    "assistant",
    "specialist",      # too junior
    "sourcer",
    "recruiter",       # individual contributor, not manager
    "sales",
    "marketing",
    "engineer",
    "developer",
    "nurse",
    "physician",
    "clinical",
    "medical",
    "accounting",
    "finance",
    "legal",
    "custod",
    "janitor",
    "warehouse",
    "driver",
    "mechanic",
    "technician",
]

# ─── Location Filtering ──────────────────────────────────────────────

# Only keep jobs whose location matches one of these patterns (case-insensitive)
# Jobs with no location info will also be kept (benefit of the doubt)
LOCATION_MUST_MATCH = [
    "san francisco",
    "sf",
    "bay area",
    "oakland",
    "san jose",
    "palo alto",
    "mountain view",
    "sunnyvale",
    "santa clara",
    "redwood city",
    "menlo park",
    "fremont",
    "berkeley",
    "san mateo",
    "cupertino",
    "milpitas",
    "hayward",
    "pleasanton",
    "walnut creek",
    "concord",
    "daly city",
    "south san francisco",
    "foster city",
    "burlingame",
    "san ramon",
    "livermore",
    "dublin",
    "alameda",
    "emeryville",
    "remote",
    "anywhere",
    "united states",
    "usa",
    "us",
    "hybrid",
    "california",
    "ca",
]

# ─── Email Settings ────────────────────────────────────────────────────

RECIPIENT_EMAIL = "rajvaitalent@gmail.com"
SENDER_EMAIL = "rajvaitalent@gmail.com"  # Will be updated based on email method

# ─── File Paths ────────────────────────────────────────────────────────

SEEN_JOBS_FILE = "data/seen_jobs.json"

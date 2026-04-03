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

# ─── Email Settings ────────────────────────────────────────────────────

RECIPIENT_EMAIL = "rajvaitalent@gmail.com"
SENDER_EMAIL = "rajvaitalent@gmail.com"  # Will be updated based on email method

# ─── File Paths ────────────────────────────────────────────────────────

SEEN_JOBS_FILE = "data/seen_jobs.json"

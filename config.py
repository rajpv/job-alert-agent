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

# ─── Location Filtering (WHITELIST-ONLY approach) ────────────────────
# A job is ONLY accepted if its location explicitly matches a US location.
# Everything else is rejected — no blocklist needed.

# US State abbreviations — used with comma prefix to avoid false matches
# e.g., ", CA" matches "San Francisco, CA" but not "Cairo"
US_STATE_ABBREVIATIONS = [
    ", al", ", ak", ", az", ", ar", ", ca", ", co", ", ct", ", de", ", fl",
    ", ga", ", hi", ", id", ", il", ", in", ", ia", ", ks", ", ky", ", la",
    ", me", ", md", ", ma", ", mi", ", mn", ", ms", ", mo", ", mt", ", ne",
    ", nv", ", nh", ", nj", ", nm", ", ny", ", nc", ", nd", ", oh", ", ok",
    ", or", ", pa", ", ri", ", sc", ", sd", ", tn", ", tx", ", ut", ", vt",
    ", va", ", wa", ", wv", ", wi", ", wy", ", dc",
]

# Full US state names
US_STATE_NAMES = [
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
    "maine", "maryland", "massachusetts", "michigan", "minnesota",
    "mississippi", "missouri", "montana", "nebraska", "nevada",
    "new hampshire", "new jersey", "new mexico", "new york",
    "north carolina", "north dakota", "ohio", "oklahoma", "oregon",
    "pennsylvania", "rhode island", "south carolina", "south dakota",
    "tennessee", "texas", "utah", "vermont", "virginia", "washington",
    "west virginia", "wisconsin", "wyoming", "district of columbia",
]

# SF Bay Area cities — all major cities across 9 Bay Area counties
# Counties: San Francisco, San Mateo, Santa Clara, Alameda, Contra Costa,
#           Marin, Sonoma, Napa, Solano
BAY_AREA_CITIES = [
    # General terms
    "bay area",
    "sf bay",
    "silicon valley",
    # ── San Francisco County ──
    "san francisco",
    "south san francisco",
    # ── San Mateo County ──
    "san mateo",
    "redwood city",
    "daly city",
    "foster city",
    "burlingame",
    "menlo park",
    "san carlos",
    "belmont",
    "san bruno",
    "pacifica",
    "half moon bay",
    "millbrae",
    "colma",
    "hillsborough",
    "atherton",
    "woodside",
    "portola valley",
    "east palo alto",
    "brisbane",
    "moss beach",
    "el granada",
    # ── Santa Clara County ──
    "san jose",
    "palo alto",
    "mountain view",
    "sunnyvale",
    "santa clara",
    "cupertino",
    "milpitas",
    "campbell",
    "los gatos",
    "saratoga",
    "gilroy",
    "morgan hill",
    "los altos",
    "los altos hills",
    "monte sereno",
    # ── Alameda County ──
    "oakland",
    "fremont",
    "hayward",
    "berkeley",
    "alameda",
    "pleasanton",
    "livermore",
    "dublin, ca",
    "union city",
    "newark",
    "san leandro",
    "san lorenzo",
    "castro valley",
    "emeryville",
    "albany",
    "piedmont",
    # ── Contra Costa County ──
    "walnut creek",
    "concord",
    "san ramon",
    "richmond",
    "antioch",
    "pittsburg",
    "brentwood",
    "oakley",
    "martinez",
    "pleasant hill",
    "lafayette",
    "moraga",
    "orinda",
    "danville",
    "el cerrito",
    "hercules",
    "pinole",
    "san pablo",
    "clayton",
    # ── Marin County ──
    "san rafael",
    "novato",
    "mill valley",
    "sausalito",
    "tiburon",
    "larkspur",
    "corte madera",
    "fairfax",
    "san anselmo",
    "ross",
    "belvedere",
    "kentfield",
    "greenbrae",
    "stinson beach",
    # ── Sonoma County ──
    "santa rosa",
    "petaluma",
    "rohnert park",
    "windsor",
    "healdsburg",
    "sonoma",
    "cotati",
    "cloverdale",
    "sebastopol",
    # ── Napa County ──
    "napa",
    "american canyon",
    "st. helena",
    "calistoga",
    "yountville",
    # ── Solano County ──
    "vallejo",
    "fairfield",
    "vacaville",
    "benicia",
    "suisun city",
    "dixon",
    "rio vista",
    # ── Nearby / Extended Bay Area ──
    "santa cruz",
    "scotts valley",
    "watsonville",
    "tracy",
    "manteca",
    "stockton",
]

# US-specific keywords that confirm a US location
US_KEYWORDS = [
    "united states",
    "usa",
]

# Remote + US patterns that are explicitly allowed
REMOTE_US_PATTERNS = [
    "remote, us",
    "remote - us",
    "remote - united states",
    "remote, united states",
    "remote (us)",
    "remote (usa)",
    "remote (united states)",
    "remote usa",
    "united states (remote)",
    "us (remote)",
    "usa (remote)",
    "anywhere in the us",
    "anywhere in the united states",
    "remote in us",
    "remote in usa",
    "remote in united states",
]

# ─── Top 50 Bay Area Tech Companies ──────────────────────────────────
# Company-targeted searches run daily to specifically check these companies

TARGET_COMPANIES = [
    # Tier 1 - Mega Cap
    "Google",
    "Apple",
    "Meta",
    "NVIDIA",
    "Salesforce",
    "Adobe",
    "Oracle",
    "Tesla",
    "Broadcom",
    "Cisco",
    # Tier 2 - Large Cap / Major Employers
    "Intel",
    "Uber",
    "LinkedIn",
    "Visa",
    "Intuit",
    "ServiceNow",
    "Palo Alto Networks",
    "Synopsys",
    "AMD",
    "PayPal",
    # Tier 3 - High Growth / Well-Known
    "OpenAI",
    "Anthropic",
    "DoorDash",
    "Pinterest",
    "Snap",
    "X",
    "Palantir",
    "Zoom",
    "Block",
    "Stripe",
    # Tier 4 - Notable / Rising
    "Airbnb",
    "Snowflake",
    "Databricks",
    "Figma",
    "Ripple",
    "Scale AI",
    "Perplexity",
    "Samsara",
    "Cloudflare",
    "Twilio",
    # Tier 5 - Established / Specialized
    "Splunk",
    "VMware",
    "Workday",
    "Fortinet",
    "Juniper Networks",
    "Nutanix",
    "Confluent",
    "HashiCorp",
    "Datadog",
    "Toast",
]

# Simplified search terms for company-targeted mode
# (fewer terms since we're combining with company name)
COMPANY_SEARCH_TERMS = [
    "Recruiting Manager",
    "Talent Acquisition Manager",
    "Talent Acquisition Director",
    "Recruiting Director",
    "Head of Talent Acquisition",
]

# Hours lookback for company-targeted searches (daily run = 24h + buffer)
COMPANY_HOURS_OLD = 48

# ─── Email Settings ────────────────────────────────────────────────────

RECIPIENT_EMAIL = "rajvaitalent@gmail.com"
SENDER_EMAIL = "rajvaitalent@gmail.com"  # Will be updated based on email method

# ─── File Paths ────────────────────────────────────────────────────────

SEEN_JOBS_FILE = "data/seen_jobs.json"

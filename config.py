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
# Jobs with NO location info will be EXCLUDED (no benefit of the doubt)
LOCATION_MUST_MATCH = [
    # SF Bay Area cities
    "san francisco",
    "south san francisco",
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
    "foster city",
    "burlingame",
    "san ramon",
    "livermore",
    "dublin, ca",
    "alameda",
    "emeryville",
    "santa cruz",
    "san rafael",
    "novato",
    "vallejo",
    "napa",
    "petaluma",
    # California state
    "california",
    ", ca",
    # Remote but US-based
    "remote, us",
    "remote - us",
    "remote - united states",
    "remote, united states",
    "remote (us)",
    "remote (united states)",
    "remote usa",
    "united states (remote)",
    "us (remote)",
    "usa (remote)",
    "anywhere in the us",
    "anywhere in the united states",
    "united states",
    # Hybrid
    "hybrid",
]

# International locations to BLOCK — if location contains any of these,
# the job is excluded even if it also matches an allowed keyword
LOCATION_BLOCKLIST = [
    # Countries
    "philippines",
    "australia",
    "spain",
    "france",
    "germany",
    "india",
    "united kingdom",
    "uk",
    "canada",
    "brazil",
    "mexico",
    "japan",
    "china",
    "singapore",
    "ireland",
    "netherlands",
    "sweden",
    "switzerland",
    "italy",
    "portugal",
    "poland",
    "argentina",
    "colombia",
    "chile",
    "israel",
    "south korea",
    "taiwan",
    "hong kong",
    "new zealand",
    "south africa",
    "nigeria",
    "kenya",
    "egypt",
    "uae",
    "dubai",
    "saudi",
    "qatar",
    "pakistan",
    "bangladesh",
    "vietnam",
    "thailand",
    "indonesia",
    "malaysia",
    # International cities
    "london",
    "toronto",
    "vancouver",
    "montreal",
    "sydney",
    "melbourne",
    "mumbai",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "delhi",
    "pune",
    "chennai",
    "noida",
    "gurgaon",
    "gurugram",
    "kolkata",
    "manila",
    "makati",
    "cebu",
    "barcelona",
    "madrid",
    "paris",
    "normandy",
    "berlin",
    "munich",
    "amsterdam",
    "dublin, ireland",
    "tokyo",
    "shanghai",
    "beijing",
    "shenzhen",
    "seoul",
    "tel aviv",
    "sao paulo",
    "rio de janeiro",
    "mexico city",
    "bogota",
    "buenos aires",
    "lima",
    "cape town",
    "johannesburg",
    "lagos",
    "nairobi",
    "cairo",
    "auckland",
    "wellington",
    "stockholm",
    "zurich",
    "geneva",
    "rome",
    "milan",
    "lisbon",
    "warsaw",
    "prague",
    "vienna",
    "brussels",
    "copenhagen",
    "helsinki",
    "oslo",
    # Regions
    "emea",
    "apac",
    "asia pacific",
    "europe",
    "latam",
    "latin america",
    "middle east",
    "africa",
    "oceania",
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

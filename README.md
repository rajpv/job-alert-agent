# Job Alert Agent

Automated job alert agent that monitors **LinkedIn**, **Indeed**, and **Google Jobs** for recruiting and talent acquisition roles in the San Francisco Bay Area. Sends email alerts via Gmail when new postings are found.

## How It Works

### Two Search Modes

| Mode | Schedule | What It Does |
|------|----------|--------------|
| **General Search** | Every 30 minutes | Broad search for all TA/recruiting roles in SF Bay Area + Remote |
| **Company-Targeted Search** | Daily at 8:00 AM PT | Searches the top 50 Bay Area tech companies specifically |

### Pipeline

1. **Scrape** job boards using `python-jobspy`
2. **Filter** by title relevance (recruiting/TA roles only) and location (Bay Area + Remote)
3. **Deduplicate** against `data/seen_jobs.json` to avoid repeat alerts
4. **Email** new postings via Gmail SMTP
5. **Commit** updated state back to the repo

### Top 50 Target Companies

Google, Apple, Meta, NVIDIA, Salesforce, Adobe, Oracle, Tesla, Broadcom, Cisco, Intel, Uber, LinkedIn, Visa, Intuit, ServiceNow, Palo Alto Networks, Synopsys, AMD, PayPal, OpenAI, Anthropic, DoorDash, Pinterest, Snap, X, Palantir, Zoom, Block, Stripe, Airbnb, Snowflake, Databricks, Figma, Ripple, Scale AI, Perplexity, Samsara, Cloudflare, Twilio, Splunk, VMware, Workday, Fortinet, Juniper Networks, Nutanix, Confluent, HashiCorp, Datadog, Toast

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/rajpv/job-alert-agent.git
cd job-alert-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your search

Edit `config.py` to customize:
- `SEARCH_QUERIES` — job titles to search for
- `LOCATIONS` — geographic areas to target
- `TARGET_COMPANIES` — companies for daily targeted search
- `TITLE_MUST_CONTAIN` / `TITLE_EXCLUDE` — relevance filters
- `LOCATION_MUST_MATCH` — location whitelist

### 4. Set up Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Create an App Password for "Mail"
4. Copy the 16-character password

### 5. Add GitHub Secrets

Go to your repo → Settings → Secrets and variables → Actions:

| Secret | Value |
|--------|-------|
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | 16-character app password |

### 6. Enable GitHub Actions

The workflows will start automatically after pushing to the repo.

## Local Testing

```bash
# General search (dry run — no email)
python main.py --dry-run

# Company-targeted search (dry run)
python main.py --mode company --dry-run

# Full run with email (requires env vars)
export GMAIL_ADDRESS="your@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
python main.py
python main.py --mode company
```

## Project Structure

```
job-alert-agent/
├── .github/workflows/
│   ├── job_alert.yml         # General search (every 30 min)
│   └── company_alert.yml     # Company-targeted search (daily)
├── data/
│   └── seen_jobs.json        # Tracks previously alerted jobs
├── config.py                 # All search settings and company list
├── scraper.py                # Job scraping + filtering engine
├── notifier.py               # Email notification system
├── state.py                  # Duplicate detection / state management
├── main.py                   # Main entry point / pipeline orchestrator
└── requirements.txt          # Python dependencies
```

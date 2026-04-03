# Job Alert Agent

An automated agent that monitors **LinkedIn**, **Indeed**, and **Google Jobs** for new job postings and sends email alerts via Gmail every 30 minutes.

## How It Works

1. **Scrapes** job boards for specified roles and locations using [python-jobspy](https://github.com/speedyapply/JobSpy)
2. **Deduplicates** results against previously seen jobs (stored in `data/seen_jobs.json`)
3. **Emails** only the new postings as a formatted HTML alert via Gmail SMTP
4. **Runs automatically** every 30 minutes via GitHub Actions

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/job-alert-agent.git
cd job-alert-agent
pip install -r requirements.txt
```

### 2. Configure your search (edit `config.py`)

- `SEARCH_QUERIES` — Job titles to search for
- `LOCATIONS` — Target locations
- `SITES` — Job boards to scrape
- `HOURS_OLD` — How far back to look (in hours)
- `RECIPIENT_EMAIL` — Where to send alerts

### 3. Set up Gmail App Password

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Create an App Password for "Mail"
4. Save the 16-character password

### 4. Add GitHub Secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|---|---|
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | The 16-character app password |

### 5. Enable GitHub Actions

The workflow runs automatically every 30 minutes. You can also trigger it manually from the **Actions** tab.

## Local Testing

```bash
# Dry run (scrape + deduplicate, no email)
python main.py --dry-run

# Full run (requires GMAIL_APP_PASSWORD env var)
export GMAIL_ADDRESS="your.email@gmail.com"
export GMAIL_APP_PASSWORD="your-app-password"
python main.py
```

## Project Structure

```
job-alert-agent/
├── .github/workflows/
│   └── job_alert.yml      # GitHub Actions schedule (every 30 min)
├── data/
│   └── seen_jobs.json     # Tracks previously alerted jobs
├── config.py              # Search settings and email config
├── scraper.py             # Job scraping engine
├── notifier.py            # Email notification system
├── state.py               # Duplicate detection / state management
├── main.py                # Main entry point (orchestrator)
└── requirements.txt       # Python dependencies
```

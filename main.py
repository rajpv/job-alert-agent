"""
Job Alert Agent — Main Entry Point
===================================
Orchestrates the full pipeline:
  1. Scrape jobs from LinkedIn, Indeed, and Google Jobs
  2. Filter out previously seen jobs (duplicate detection)
  3. Send email alert with only the new postings

Usage:
  python main.py                        # General search (30-min cycle)
  python main.py --mode company         # Company-targeted search (daily)
  python main.py --dry-run              # General search, no email
  python main.py --mode company --dry-run  # Company-targeted, no email
"""

import sys
import csv
from datetime import datetime
from scraper import fetch_all_jobs, fetch_company_targeted_jobs
from state import filter_new_jobs
from notifier import send_email_alert


def run(mode: str = "general", dry_run: bool = False):
    """
    Execute the full job alert pipeline.

    Args:
        mode: "general" for broad role-based search,
              "company" for company-targeted search
        dry_run: If True, skip sending email
    """
    mode_label = "GENERAL SEARCH" if mode == "general" else "COMPANY-TARGETED SEARCH (Top 50)"
    print("=" * 60)
    print(f"  JOB ALERT AGENT — {mode_label}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ── Step 1: Scrape jobs ──────────────────────────────────────
    print(f"\n📡 Step 1: Scraping job boards ({mode} mode)...")

    if mode == "company":
        all_jobs = fetch_company_targeted_jobs()
    else:
        all_jobs = fetch_all_jobs()

    if all_jobs.empty:
        print("\nNo jobs found in this run. Exiting.")
        return

    # ── Step 2: Filter duplicates ────────────────────────────────
    print("\n🔍 Step 2: Checking for new jobs...")
    new_jobs = filter_new_jobs(all_jobs)

    if new_jobs.empty:
        print("\nNo new jobs since last check. Exiting.")
        return

    # ── Step 3: Send email alert ─────────────────────────────────
    # Customize subject line based on mode
    subject_prefix = "🏢 Top Company" if mode == "company" else "🔔"
    email_subject = f"{subject_prefix} Job Alert: {len(new_jobs)} New Posting{'s' if len(new_jobs) != 1 else ''}"

    print(f"\n📧 Step 3: Sending alert for {len(new_jobs)} new jobs...")

    if dry_run:
        print("  [DRY RUN] Skipping email. Here are the new jobs:")
        for _, job in new_jobs.iterrows():
            company_tag = ""
            if "target_company" in job and not __import__("pandas").isna(job.get("target_company")):
                company_tag = f" [Target: {job['target_company']}]"
            print(f"  • {job.get('title', 'N/A')} at {job.get('company', 'N/A')}{company_tag} ({job.get('site', 'N/A')})")
            print(f"    {job.get('job_url', 'N/A')}")
    else:
        success = send_email_alert(new_jobs, subject=email_subject)
        if not success:
            print("  Failed to send email alert.")
            sys.exit(1)

    # ── Save a CSV log of this run ───────────────────────────────
    log_suffix = f"_{mode}" if mode == "company" else ""
    log_file = f"data/jobs_log_{datetime.now().strftime('%Y%m%d')}{log_suffix}.csv"
    try:
        new_jobs.to_csv(log_file, mode="a", header=not __import__("os").path.exists(log_file),
                        index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")
        print(f"\n📋 Jobs logged to {log_file}")
    except Exception as e:
        print(f"  Warning: Could not save log: {e}")

    print("\n✅ Done!")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    mode = "company" if "--mode" in sys.argv and "company" in sys.argv else "general"
    run(mode=mode, dry_run=dry_run)

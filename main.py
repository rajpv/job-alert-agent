"""
Job Alert Agent — Main Entry Point
===================================
Orchestrates the full pipeline:
  1. Scrape jobs from LinkedIn, Indeed, and Google Jobs
  2. Filter out previously seen jobs (duplicate detection)
  3. Send email alert with only the new postings

Usage:
  python main.py              # Run the full pipeline
  python main.py --dry-run    # Scrape and detect new jobs, but don't send email
"""

import sys
import csv
from datetime import datetime
from scraper import fetch_all_jobs
from state import filter_new_jobs
from notifier import send_email_alert


def run(dry_run: bool = False):
    """
    Execute the full job alert pipeline.
    """
    print("=" * 60)
    print(f"  JOB ALERT AGENT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ── Step 1: Scrape jobs ──────────────────────────────────────
    print("\n📡 Step 1: Scraping job boards...")
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
    print(f"\n📧 Step 3: Sending alert for {len(new_jobs)} new jobs...")

    if dry_run:
        print("  [DRY RUN] Skipping email. Here are the new jobs:")
        for _, job in new_jobs.iterrows():
            print(f"  • {job.get('title', 'N/A')} at {job.get('company', 'N/A')} ({job.get('site', 'N/A')})")
            print(f"    {job.get('job_url', 'N/A')}")
    else:
        success = send_email_alert(new_jobs)
        if not success:
            print("  Failed to send email alert.")
            sys.exit(1)

    # ── Save a CSV log of this run ───────────────────────────────
    log_file = f"data/jobs_log_{datetime.now().strftime('%Y%m%d')}.csv"
    try:
        new_jobs.to_csv(log_file, mode="a", header=not __import__("os").path.exists(log_file),
                        index=False, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")
        print(f"\n📋 Jobs logged to {log_file}")
    except Exception as e:
        print(f"  Warning: Could not save log: {e}")

    print("\n✅ Done!")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run(dry_run=dry_run)

"""
State Management Module
Tracks which jobs have already been seen to prevent duplicate alerts.
Uses a JSON file to persist state across runs.
"""

import json
import os
from datetime import datetime, timedelta
import pandas as pd
import config


def load_seen_jobs() -> dict:
    """
    Load the set of previously seen job URLs from the JSON file.
    Returns a dict of {job_url: timestamp_first_seen}.
    """
    filepath = config.SEEN_JOBS_FILE
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not read seen_jobs file. Starting fresh.")
            return {}
    return {}


def save_seen_jobs(seen_jobs: dict) -> None:
    """
    Save the seen jobs dict to the JSON file.
    """
    filepath = config.SEEN_JOBS_FILE

    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w") as f:
        json.dump(seen_jobs, f, indent=2)


def cleanup_old_entries(seen_jobs: dict, days: int = 30) -> dict:
    """
    Remove entries older than `days` to keep the file from growing forever.
    """
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    cleaned = {url: ts for url, ts in seen_jobs.items() if ts >= cutoff}

    removed = len(seen_jobs) - len(cleaned)
    if removed > 0:
        print(f"  Cleaned up {removed} job entries older than {days} days")

    return cleaned


def filter_new_jobs(jobs_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare scraped jobs against the seen-jobs state.
    Returns a DataFrame containing only jobs we haven't seen before.
    Also updates the state file with the new jobs.
    """
    if jobs_df.empty:
        return jobs_df

    # Load existing state
    seen_jobs = load_seen_jobs()

    # Clean up old entries periodically
    seen_jobs = cleanup_old_entries(seen_jobs)

    # Filter out already-seen jobs
    new_mask = ~jobs_df["job_url"].isin(seen_jobs.keys())
    new_jobs = jobs_df[new_mask].copy()

    # Record the new jobs in state
    now = datetime.now().isoformat()
    for url in new_jobs["job_url"]:
        seen_jobs[url] = now

    # Save updated state
    save_seen_jobs(seen_jobs)

    seen_count = len(jobs_df) - len(new_jobs)
    if seen_count > 0:
        print(f"  Filtered out {seen_count} previously seen jobs")
    print(f"  {len(new_jobs)} genuinely new jobs to alert on")

    return new_jobs


if __name__ == "__main__":
    # Test the state management
    print("=" * 60)
    print("STATE MANAGEMENT - TEST")
    print("=" * 60)

    # Simulate some jobs
    sample = pd.DataFrame({
        "job_url": [
            "https://linkedin.com/jobs/111",
            "https://indeed.com/jobs/222",
            "https://linkedin.com/jobs/333",
        ],
        "title": ["Job A", "Job B", "Job C"],
        "site": ["linkedin", "indeed", "linkedin"],
    })

    print("\nRun 1: All jobs should be new")
    new = filter_new_jobs(sample)
    print(f"  Result: {len(new)} new jobs\n")

    print("Run 2: Same jobs — all should be filtered out")
    new = filter_new_jobs(sample)
    print(f"  Result: {len(new)} new jobs\n")

    # Add one new job
    sample2 = pd.DataFrame({
        "job_url": [
            "https://linkedin.com/jobs/111",  # already seen
            "https://indeed.com/jobs/444",     # new!
        ],
        "title": ["Job A", "Job D"],
        "site": ["linkedin", "indeed"],
    })

    print("Run 3: Mix of old and new — only 1 should be new")
    new = filter_new_jobs(sample2)
    print(f"  Result: {len(new)} new jobs")
    print(f"  New job: {new['title'].values}")

    # Cleanup test file
    if os.path.exists(config.SEEN_JOBS_FILE):
        os.remove(config.SEEN_JOBS_FILE)
        print("\nTest state file cleaned up.")

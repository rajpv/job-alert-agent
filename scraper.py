"""
Job Scraper Module
Fetches job postings from LinkedIn, Indeed, and Google Jobs
using the python-jobspy library.
"""

import pandas as pd
from jobspy import scrape_jobs
import config


def fetch_jobs_for_query(search_term: str, location: str) -> pd.DataFrame:
    """
    Scrape jobs for a single search term and location combination.
    Returns a DataFrame of job postings.
    """
    all_results = []

    # Scrape each site individually so one failure doesn't block others
    for site in config.SITES:
        try:
            kwargs = {
                "site_name": [site],
                "search_term": search_term,
                "location": location,
                "results_wanted": config.RESULTS_WANTED,
                "hours_old": config.HOURS_OLD,
                "country_indeed": config.COUNTRY_INDEED,
                "verbose": 0,
            }
            # Google Jobs needs a special search term
            if site == "google":
                kwargs["google_search_term"] = (
                    f"{search_term} jobs near {location} since yesterday"
                )

            df = scrape_jobs(**kwargs)
            if not df.empty:
                all_results.append(df)

        except Exception as e:
            print(f"    ⚠ {site} error: {e}")

    if all_results:
        return pd.concat(all_results, ignore_index=True)
    return pd.DataFrame()


def fetch_all_jobs() -> pd.DataFrame:
    """
    Run all search query + location combinations and return
    a single deduplicated DataFrame of results.
    """
    all_jobs = []

    for search_term in config.SEARCH_QUERIES:
        for location in config.LOCATIONS:
            print(f"  Searching: '{search_term}' in '{location}'...")
            df = fetch_jobs_for_query(search_term, location)
            if not df.empty:
                print(f"    Found {len(df)} jobs")
                all_jobs.append(df)
            else:
                print(f"    No jobs found")

    if not all_jobs:
        print("No jobs found across all searches.")
        return pd.DataFrame()

    # Combine all results
    combined = pd.concat(all_jobs, ignore_index=True)

    # Deduplicate by job_url (same job may appear in multiple searches)
    before_dedup = len(combined)
    combined = combined.drop_duplicates(subset=["job_url"], keep="first")
    after_dedup = len(combined)

    if before_dedup != after_dedup:
        print(f"  Removed {before_dedup - after_dedup} duplicate listings")

    print(f"\nTotal unique jobs found: {len(combined)}")
    return combined


if __name__ == "__main__":
    # Quick test: run the scraper standalone
    print("=" * 60)
    print("JOB SCRAPER - TEST RUN")
    print("=" * 60)
    jobs = fetch_all_jobs()
    if not jobs.empty:
        print("\nSample results:")
        print(jobs[["site", "title", "company", "location", "job_url"]].head(10).to_string())
    else:
        print("No jobs found.")

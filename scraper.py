"""
Job Scraper Module
Fetches job postings from LinkedIn, Indeed, and Google Jobs
using the python-jobspy library, then filters for relevance
and location.
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


def filter_by_title_relevance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter jobs to only include relevant recruiting/TA titles.
    - Title MUST contain at least one keyword from TITLE_MUST_CONTAIN
    - Title must NOT contain any keyword from TITLE_EXCLUDE
    """
    if df.empty or "title" not in df.columns:
        return df

    must_contain = config.TITLE_MUST_CONTAIN
    exclude = config.TITLE_EXCLUDE

    def is_relevant(title):
        if pd.isna(title):
            return False
        title_lower = str(title).lower()

        # Must contain at least one relevant keyword
        has_relevant = any(kw in title_lower for kw in must_contain)
        if not has_relevant:
            return False

        # Must NOT contain any excluded keyword
        has_excluded = any(kw in title_lower for kw in exclude)
        if has_excluded:
            return False

        return True

    before = len(df)
    df = df[df["title"].apply(is_relevant)].copy()
    after = len(df)

    if before != after:
        print(f"    Title filter: {before} → {after} jobs ({before - after} removed)")

    return df


def filter_by_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter jobs to only include those in the SF Bay Area or Remote.
    Jobs with no location info are kept (benefit of the doubt).
    """
    if df.empty or "location" not in df.columns:
        return df

    allowed = config.LOCATION_MUST_MATCH

    def location_matches(loc):
        if pd.isna(loc) or str(loc).strip() == "":
            return True  # Keep jobs with no location (benefit of the doubt)
        loc_lower = str(loc).lower()
        return any(kw in loc_lower for kw in allowed)

    before = len(df)
    df = df[df["location"].apply(location_matches)].copy()
    after = len(df)

    if before != after:
        print(f"    Location filter: {before} → {after} jobs ({before - after} removed)")

    return df


def fetch_all_jobs() -> pd.DataFrame:
    """
    Run all search query + location combinations and return
    a single deduplicated DataFrame of results, filtered for
    relevance and location.
    """
    all_jobs = []

    for search_term in config.SEARCH_QUERIES:
        for location in config.LOCATIONS:
            print(f"  Searching: '{search_term}' in '{location}'...")
            df = fetch_jobs_for_query(search_term, location)
            if not df.empty:
                print(f"    Found {len(df)} raw jobs")
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

    print(f"\nTotal unique jobs before filtering: {len(combined)}")

    # ── Apply relevance filters ──────────────────────────────────
    print("\n🎯 Applying relevance filters...")
    combined = filter_by_title_relevance(combined)
    combined = filter_by_location(combined)

    print(f"\nTotal relevant jobs after filtering: {len(combined)}")
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

"""
Job Scraper Module
Fetches job postings from LinkedIn, Indeed, and Google Jobs
using the python-jobspy library, then filters for relevance
and location.

Supports two modes:
  - General search: broad role-based searches (every 30 min)
  - Company-targeted search: role + company name (daily)
"""

import re
import time
import random
import pandas as pd
from jobspy import scrape_jobs
import config


def fetch_jobs_for_query(search_term: str, location: str,
                         hours_old: int = None,
                         sites: list = None) -> pd.DataFrame:
    """
    Scrape jobs for a single search term and location combination.
    Returns a DataFrame of job postings.
    """
    all_results = []
    sites = sites or config.SITES
    hours_old = hours_old or config.HOURS_OLD

    # Scrape each site individually so one failure doesn't block others
    for site in sites:
        try:
            kwargs = {
                "site_name": [site],
                "search_term": search_term,
                "location": location,
                "results_wanted": config.RESULTS_WANTED,
                "hours_old": hours_old,
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
    WHITELIST-ONLY location filter.
    A job is ONLY accepted if its location explicitly matches a known
    US location. Everything else is rejected — no blocklist needed.

    Logic:
    1. No location → REJECT
    2. Contains "remote" → only accept if also has US qualifier
    3. Contains a Bay Area city name → ACCEPT
    4. Contains a US state abbreviation (", CA", ", NY") → ACCEPT
    5. Contains a US state full name → ACCEPT
    6. Contains "united states" or "usa" → ACCEPT
    7. Everything else → REJECT
    """
    if df.empty or "location" not in df.columns:
        return df

    def _has_us_state_abbr(loc_lower):
        """
        Check if location contains a US state abbreviation like ', CA'
        at the END of the string or followed by a space/comma.
        Uses regex to avoid false matches like 'Alberta, Canada' matching ', CA'.
        """
        for abbr in config.US_STATE_ABBREVIATIONS:
            # Extract the 2-letter state code (e.g., 'ca' from ', ca')
            state_code = abbr.strip().lstrip(','). strip()
            # Match: comma + optional space + 2-letter code at end of string
            # or followed by space/comma (not more letters)
            pattern = rf',\s*{re.escape(state_code)}(?:\s*$|\s|,)'
            if re.search(pattern, loc_lower):
                return True
        return False

    def _has_us_indicator(loc_lower):
        """
        Check if location has any US indicator:
        state abbreviation, state name, Bay Area city, or US keyword.
        """
        if _has_us_state_abbr(loc_lower):
            return True
        for state in config.US_STATE_NAMES:
            if state in loc_lower:
                return True
        for city in config.BAY_AREA_CITIES:
            if city in loc_lower:
                return True
        for kw in config.US_KEYWORDS:
            if kw in loc_lower:
                return True
        return False

    def is_us_location(loc):
        # Step 1: No location → reject
        if pd.isna(loc) or str(loc).strip() == "":
            return False

        loc_lower = str(loc).lower().strip()

        # Step 2: Handle "remote" locations
        if "remote" in loc_lower:
            # Check for explicit US remote patterns
            for pattern in config.REMOTE_US_PATTERNS:
                if pattern in loc_lower:
                    return True
            # Check for any US indicator
            if _has_us_indicator(loc_lower):
                return True
            # Bare "remote" with no US context → REJECT
            return False

        # Step 3: Check Bay Area cities (primary target)
        for city in config.BAY_AREA_CITIES:
            if city in loc_lower:
                return True

        # Step 4: Check US state abbreviations with strict matching
        if _has_us_state_abbr(loc_lower):
            return True

        # Step 5: Check US state full names
        for state in config.US_STATE_NAMES:
            if state in loc_lower:
                return True

        # Step 6: Check US keywords ("united states", "usa")
        for kw in config.US_KEYWORDS:
            if kw in loc_lower:
                return True

        # Step 7: Everything else → REJECT
        return False

    before = len(df)

    # Log rejected locations for debugging
    rejected = df[~df["location"].apply(is_us_location)]
    if not rejected.empty:
        print(f"    Locations REJECTED (not US):")
        for loc in rejected["location"].unique():
            print(f"      ✗ {loc}")

    # Log accepted locations
    accepted = df[df["location"].apply(is_us_location)]
    if not accepted.empty:
        print(f"    Locations ACCEPTED (US confirmed):")
        for loc in accepted["location"].unique():
            print(f"      ✓ {loc}")

    df = accepted.copy()
    after = len(df)

    if before != after:
        print(f"    Location filter: {before} → {after} jobs ({before - after} removed)")

    return df


def fetch_all_jobs() -> pd.DataFrame:
    """
    GENERAL MODE: Run all search query + location combinations and return
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


def fetch_company_targeted_jobs() -> pd.DataFrame:
    """
    COMPANY-TARGETED MODE: Search for recruiting/TA roles at each
    of the top 50 Bay Area tech companies. Uses company name in
    the search query for precision.

    Runs with human-like pacing to avoid rate limiting.
    """
    all_jobs = []
    total_companies = len(config.TARGET_COMPANIES)
    batch_size = 25

    for i, company in enumerate(config.TARGET_COMPANIES, 1):
        print(f"\n  [{i}/{total_companies}] 🏢 {company}")

        for search_term in config.COMPANY_SEARCH_TERMS:
            query = f"{search_term} {company}"
            print(f"    Searching: '{query}'...")

            df = fetch_jobs_for_query(
                search_term=query,
                location="San Francisco Bay Area, CA",
                hours_old=config.COMPANY_HOURS_OLD,
            )

            if not df.empty:
                # Tag the source company for tracking
                df["target_company"] = company
                print(f"      Found {len(df)} raw jobs")
                all_jobs.append(df)
            else:
                print(f"      No jobs found")

            # Human-like pacing: randomized wait between queries
            wait_time = random.uniform(2, 5)
            time.sleep(wait_time)

        # After every batch of 25 companies, take a longer pause
        if i % batch_size == 0 and i < total_companies:
            pause = random.uniform(30, 60)
            print(f"\n  ⏸  Batch pause ({pause:.0f}s) to avoid rate limits...")
            time.sleep(pause)

    if not all_jobs:
        print("No jobs found across company-targeted searches.")
        return pd.DataFrame()

    # Combine all results
    combined = pd.concat(all_jobs, ignore_index=True)

    # Deduplicate by job_url
    before_dedup = len(combined)
    combined = combined.drop_duplicates(subset=["job_url"], keep="first")
    after_dedup = len(combined)

    if before_dedup != after_dedup:
        print(f"\n  Removed {before_dedup - after_dedup} duplicate listings")

    print(f"\nTotal unique jobs before filtering: {len(combined)}")

    # ── Apply relevance filters ──────────────────────────────────
    print("\n🎯 Applying relevance filters...")
    combined = filter_by_title_relevance(combined)
    combined = filter_by_location(combined)

    print(f"\nTotal relevant jobs after filtering: {len(combined)}")
    return combined


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "general"

    print("=" * 60)
    print(f"JOB SCRAPER - TEST RUN (mode: {mode})")
    print("=" * 60)

    if mode == "company":
        jobs = fetch_company_targeted_jobs()
    else:
        jobs = fetch_all_jobs()

    if not jobs.empty:
        print("\nSample results:")
        cols = ["site", "title", "company", "location", "job_url"]
        if "target_company" in jobs.columns:
            cols.insert(0, "target_company")
        print(jobs[cols].head(10).to_string())
    else:
        print("No jobs found.")

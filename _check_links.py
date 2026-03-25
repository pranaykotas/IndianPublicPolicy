"""
Checks all project URLs in _data/projects.yml for dead links.

Usage:
  python3 _check_links.py              # check all URLs
  python3 _check_links.py --summary    # print summary only (no per-URL output)

Exit codes:
  0 — all URLs OK (or only excepted)
  1 — one or more dead links found
"""

import argparse
import sys
import time
from pathlib import Path

import requests
import yaml

TIMEOUT = 10          # seconds per request
RETRY_WAIT = 3        # seconds between retries
MAX_RETRIES = 2       # attempts before marking dead

# Status codes treated as success
OK_CODES = {200, 201, 202, 203, 204, 206, 301, 302, 303, 307, 308}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; AIforPublicPolicyBot/1.0; "
        "+https://github.com/pranaykotas/IndianPublicPolicy)"
    )
}


def load_exceptions() -> set:
    path = Path("_data/link_exceptions.yml")
    if not path.exists():
        return set()
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return set(data.get("exceptions", []))


def check_url(url: str) -> tuple[bool, int | str]:
    """Returns (ok, status_code_or_error_message)."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.head(
                url, headers=HEADERS, timeout=TIMEOUT,
                allow_redirects=True
            )
            # Some servers reject HEAD — fall back to GET
            if resp.status_code in (405, 403):
                resp = requests.get(
                    url, headers=HEADERS, timeout=TIMEOUT,
                    allow_redirects=True, stream=True
                )
            if resp.status_code in OK_CODES:
                return True, resp.status_code
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_WAIT)
        except requests.exceptions.ConnectionError:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_WAIT)
            else:
                return False, "connection error"
        except requests.exceptions.Timeout:
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_WAIT)
            else:
                return False, "timeout"
        except requests.exceptions.RequestException as e:
            return False, str(e)
    return False, resp.status_code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    # Load projects
    with open("_data/projects.yml") as f:
        projects = yaml.safe_load(f) or []

    exceptions = load_exceptions()

    results = {"ok": [], "dead": [], "excepted": []}

    for p in projects:
        name = p.get("name", "Unknown")
        url = (p.get("url") or "").strip()

        if not url:
            results["dead"].append((name, url, "missing URL"))
            continue

        if url in exceptions:
            results["excepted"].append((name, url))
            if not args.summary:
                print(f"  SKIP  {name} — {url} (in exceptions list)")
            continue

        ok, status = check_url(url)
        if ok:
            results["ok"].append((name, url, status))
            if not args.summary:
                print(f"  OK    [{status}] {name} — {url}")
        else:
            results["dead"].append((name, url, status))
            print(f"  DEAD  [{status}] {name} — {url}")

    # Summary
    total = len(projects)
    n_ok = len(results["ok"])
    n_dead = len(results["dead"])
    n_skip = len(results["excepted"])

    print(f"\n── Link check summary ──────────────────")
    print(f"  Total:    {total}")
    print(f"  OK:       {n_ok}")
    print(f"  Dead:     {n_dead}")
    print(f"  Skipped:  {n_skip} (exceptions)")

    if results["dead"]:
        print("\nDead links:")
        for name, url, status in results["dead"]:
            print(f"  • {name}: {url}  [{status}]")
        sys.exit(1)


if __name__ == "__main__":
    main()

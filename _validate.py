"""
Validates _data/projects.yml against the directory schema.
Run locally: python3 _validate.py
Also runs as a CI check on every pull request.
"""

import re
import sys
import yaml
from pathlib import Path

ALLOWED_CATEGORIES = {
    "Visualisations",
    "Analytical Tools",
    "AI Reports",
    "Admin Tools",
    "Simulations & Games",
    "Other",
}

MIN_TAGS = 2
MAX_TAGS = 5
MAX_DESCRIPTION_CHARS = 200
URL_PATTERN = re.compile(r"^https?://[^\s]+$")

errors = []


def fail(entry_index, name, message):
    label = f"Entry {entry_index + 1}" + (f' ("{name}")' if name else "")
    errors.append(f"  {label}: {message}")


# ── Load file ──────────────────────────────────────────────────────────────────

path = Path("_data/projects.yml")
if not path.exists():
    print("ERROR: _data/projects.yml not found.")
    sys.exit(1)

with open(path) as f:
    try:
        projects = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"ERROR: Could not parse YAML.\n{e}")
        sys.exit(1)

if not isinstance(projects, list) or len(projects) == 0:
    print("ERROR: projects.yml must be a non-empty YAML list.")
    sys.exit(1)

# ── Per-entry validation ───────────────────────────────────────────────────────

seen_names = {}
seen_urls = {}

for i, p in enumerate(projects):
    name = p.get("name", "").strip() if isinstance(p.get("name"), str) else ""

    # Required fields
    for field in ("name", "category", "description", "url", "tags"):
        if field not in p or p[field] is None:
            fail(i, name, f"missing required field `{field}`")
        elif isinstance(p[field], str) and not p[field].strip():
            fail(i, name, f"`{field}` is empty")

    # Category
    category = p.get("category", "")
    if category and category not in ALLOWED_CATEGORIES:
        fail(
            i,
            name,
            f'`category` must be one of: {", ".join(sorted(ALLOWED_CATEGORIES))}. '
            f'Got: "{category}"',
        )

    # Description length
    description = p.get("description", "") or ""
    if len(description) > MAX_DESCRIPTION_CHARS:
        fail(
            i,
            name,
            f"`description` is {len(description)} characters (max {MAX_DESCRIPTION_CHARS})",
        )

    # URL format
    url = p.get("url", "") or ""
    if url and not URL_PATTERN.match(url):
        fail(i, name, f'`url` does not look like a valid URL: "{url}"')

    # Tags
    tags = p.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            fail(i, name, "`tags` must be a YAML list")
        else:
            if len(tags) < MIN_TAGS:
                fail(i, name, f"`tags` must have at least {MIN_TAGS} items (got {len(tags)})")
            if len(tags) > MAX_TAGS:
                fail(i, name, f"`tags` must have at most {MAX_TAGS} items (got {len(tags)})")
            for tag in tags:
                if not isinstance(tag, str) or not tag.strip():
                    fail(i, name, f"each tag must be a non-empty string (found: {tag!r})")
                elif tag != tag.lower():
                    fail(i, name, f'tag "{tag}" must be lowercase')
                elif " " in tag:
                    fail(i, name, f'tag "{tag}" must use hyphens instead of spaces')

    # Duplicate names
    if name:
        norm_name = name.lower()
        if norm_name in seen_names:
            fail(
                i,
                name,
                f'duplicate name — same as entry {seen_names[norm_name] + 1} ("{projects[seen_names[norm_name]]["name"]}")',
            )
        else:
            seen_names[norm_name] = i

    # Duplicate URLs
    if url:
        norm_url = url.rstrip("/").lower()
        if norm_url in seen_urls:
            fail(
                i,
                name,
                f'duplicate URL — same as entry {seen_urls[norm_url] + 1} ("{projects[seen_urls[norm_url]]["name"]}")',
            )
        else:
            seen_urls[norm_url] = i

# ── Report ─────────────────────────────────────────────────────────────────────

if errors:
    print(f"Validation failed — {len(errors)} error(s) in _data/projects.yml:\n")
    for e in errors:
        print(e)
    print(
        "\nSee CONTRIBUTING.md for field rules and allowed category values."
    )
    sys.exit(1)
else:
    print(f"Validation passed — {len(projects)} project(s) OK.")

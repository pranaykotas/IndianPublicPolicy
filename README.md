# AI for Public Policy Directory

A community-curated, searchable directory of AI tools, dashboards, and projects built for public policy.

**Website:** [aipublicpolicy.org](https://aipublicpolicy.org)

## Why this exists

Many individuals and organisations are building AI-powered tools for public policy — parliamentary trackers, budget visualisers, regulation monitors, citizen tools, and more. But there is no single place to discover all of them.

This directory aims to be that place: a simple, searchable catalog where anyone working in public policy can find tools that already exist, learn from them, or build on them.

## How it works

- All projects are listed in a single YAML file ([`_data/projects.yml`](_data/projects.yml))
- The website is built with [Quarto](https://quarto.org) and deployed to GitHub Pages
- Search and tag-based filtering work entirely in the browser — no backend, no database
- Anyone can add a project by editing the YAML file and submitting a pull request
- PRs are validated automatically — entries with missing fields, bad URLs, or duplicates fail fast

## Add your project

If you've built or know of an AI tool for public policy, we'd love to include it.

1. Fork this repo
2. Add your project to `_data/projects.yml`:
   ```yaml
   - name: "Your Project Name"
     category: "Analytical Tools"
     description: "What it does and who it helps"
     url: "https://github.com/your-org/your-project"
     tags: ["tag1", "tag2", "tag3"]
   ```
3. Submit a pull request — automated checks will validate your entry

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## Run locally

You need [Quarto](https://quarto.org/docs/get-started/) and Python 3 installed.

```bash
# Install dependencies (one time)
pip install pyyaml

# Generate project HTML and preview the site
python3 _build.py && quarto preview
```

## Project structure

```
_data/
  projects.yml          # All project entries — edit this to add a project
  link_exceptions.yml   # URLs to skip during link checking
_build.py               # Generates HTML from projects.yml (pre-render)
_validate.py            # Validates projects.yml — run locally or in CI
_check_links.py         # Checks all project URLs for dead links
index.qmd               # Homepage
about.qmd               # About page
search.js               # Client-side search and filtering
styles.css              # Card grid and UI styling
CONTRIBUTING.md         # Guide for contributors
.github/workflows/
  deploy.yml            # Auto-deploy to GitHub Pages on push to main
  validate.yml          # Validates projects.yml on every PR
  check-links.yml       # Weekly dead link checker
```

## Maintained by

[Pranay Kotasthane](https://pranaykotas.com). 

## License

This directory is open source. The listing of a project here does not imply endorsement.

## Disclaimer

A project's presence on this list doesn't mean that the maintainer endorses the ideas in it. It is merely meant to be a directory. 

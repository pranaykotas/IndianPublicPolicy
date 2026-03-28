# Contributing to the AI for Public Policy Directory

Thanks for wanting to add a project! It takes about 5 minutes.

You'll be editing one file — `_data/projects.yml` — and submitting a pull request. No coding required.

---

## What can I add?

Anything that uses AI to help with public policy work. For example:

- A dashboard that tracks parliamentary proceedings
- A tool that summarises government reports
- A visualisation of budget allocations
- An assistant that helps citizens file RTI requests
- A dataset curated for policy research

It can be open-source or not, finished or in-progress, India-focused or global.

---

## Step 1: Pick your category

Every project belongs to one category. Choose the one that fits best:

| Category | What it means |
|----------|---------------|
| **Visualisations** | Live trackers and dashboards that display data in real time |
| **Analytical Tools** | Tools others can download and use for their own analysis |
| **AI Reports** | Data presented accessibly — but not updated live |
| **Admin Tools** | Tools that help think tanks and research organisations run better |
| **Simulations & Games** | Policy simulations, serious games, and interactive scenarios |
| **Other** | Doesn't fit the above? Use this |

Not sure? Pick the closest one — we can always fix it during review.

---

## Step 2: Write your entry

Open `_data/projects.yml` and add your project at the **very end** of the file.

Copy this template and fill it in:

```yaml
- name: "Your Project Name"
  category: "Analytical Tools"
  description: "One or two sentences on what it does and who it helps."
  url: "https://github.com/your-org/your-project"
  tags: ["tag1", "tag2", "tag3"]
```

**Here's a real example to copy from:**

```yaml
- name: "ParliamentWatch"
  category: "Analytical Tools"
  description: "Track, search, and get AI-powered summaries of Indian Parliamentary Committee reports from all 16 DRSCs across Lok Sabha and Rajya Sabha"
  url: "https://github.com/pranaykotas/parliamentwatch"
  tags: ["parliament", "india", "nlp", "tracking", "open-data"]
```

### Field rules

**`name`** — The project name. No need to add "AI" or "Tool" at the end.

**`category`** — Must be exactly one of: `Visualisations`, `Analytical Tools`, `AI Reports`, `Admin Tools`, `Simulations & Games`, `Other`. Spelling and capitalisation matter.

**`description`** — Keep it under 200 characters. Write what it does and who it's for — not what technology it uses.
- ✅ Good: *"Tracks new regulations across Indian ministries and classifies them by sector."*
- ❌ Bad: *"A Python-based NLP pipeline using BERT for text classification."*

**`url`** — Must start with `https://` or `http://`. Link to the GitHub repo, project website, or documentation.

**`tags`** — 2 to 5 tags, all **lowercase**, with **hyphens** instead of spaces. Browse the [directory homepage](https://aipublicpolicy.org) to see tags already in use.

> **YAML tip:** Indentation matters. Each field must be indented with exactly 2 spaces (not tabs). If in doubt, paste your entry into [yamllint.com](https://www.yamllint.com/) to check before submitting.

---

## Step 3: Submit a pull request

1. Fork this repository (click **Fork** at the top right of [this page](https://github.com/pranaykotas/IndianPublicPolicy))
2. Make your edit to `_data/projects.yml`
3. Commit with a message like: `Add ProjectName to directory`
4. Open a pull request against the `main` branch

---

## What happens after you submit

When you open a pull request, automated checks run immediately:

- **Validation** — checks that all required fields are present, the category is valid, the description isn't too long, the URL is well-formed, and there are no duplicates
- **Review** — a maintainer will review and merge, usually within a few days

If the validation check fails, you'll see a clear error message in the PR explaining what to fix. Common issues are a wrong category name or a description that's too long.

---

## Updating or removing a project

**To update** a project's URL, description, or tags: edit the entry in `_data/projects.yml` and submit a PR.

**To remove** a project: delete the entry and submit a PR, briefly explaining why (e.g. the project has shut down).

---

## Questions?

Open an [issue](https://github.com/pranaykotas/IndianPublicPolicy/issues) and we'll help.

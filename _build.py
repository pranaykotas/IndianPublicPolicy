"""Pre-render script: reads projects.yml and generates the HTML for index.qmd."""

import yaml
from pathlib import Path

with open("_data/projects.yml") as f:
    projects = yaml.safe_load(f)

category_order = ["Visualisations", "Analytical Tools", "AI Reports", "Admin Tools", "Other"]

grouped = {}
for p in projects:
    cat = p.get("category", "Other")
    if cat not in category_order:
        cat = "Other"
    grouped.setdefault(cat, []).append(p)

parts = []

parts.append('<div class="directory-container">')
parts.append('<div class="search-section">')
parts.append('  <input type="text" id="search-input" placeholder="Search projects by name or description..." />')
parts.append('  <div class="category-filters">')
parts.append('    <button class="category-btn active" data-category="all">All</button>')
for cat in category_order:
    if cat in grouped:
        parts.append(f'    <button class="category-btn" data-category="{cat}">{cat}</button>')
parts.append('  </div>')
parts.append('  <div id="tag-filters" class="tag-filters"></div>')
parts.append('  <p class="result-count"><span id="result-count"></span> projects</p>')
parts.append('</div>')

for cat in category_order:
    if cat not in grouped:
        continue
    parts.append(f'<div class="category-section" data-category="{cat}">')
    parts.append(f'  <h2 class="category-heading">{cat}</h2>')
    parts.append('  <div class="project-grid">')

    for p in grouped[cat]:
        tags_csv = ",".join(p.get("tags", []))
        tags_html = "".join(
            f'<span class="tag" data-tag="{t}">{t}</span>' for t in p.get("tags", [])
        )
        parts.append(f'''    <div class="project-card" data-tags="{tags_csv}" data-category="{cat}">
      <h3 class="project-name"><a href="{p["url"]}" target="_blank" rel="noopener">{p["name"]}</a></h3>
      <p class="project-desc">{p["description"]}</p>
      <div class="project-tags">{tags_html}</div>
    </div>''')

    parts.append('  </div>')
    parts.append('</div>')

parts.append('</div>')
parts.append('<script src="search.js"></script>')

Path("_includes").mkdir(exist_ok=True)
content = "```{=html}\n" + "\n".join(parts) + "\n```\n"
Path("_includes/projects.html").write_text(content)
print(f"Generated HTML for {len(projects)} projects")

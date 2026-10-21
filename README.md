# Denver Affordable Housing Inventory

Denver lists 29,474 income-restricted homes in 497 projects in its HOST affordable housing inventory, pulled October 21, 2026. The inventory records at least one project in 63 of 78 neighborhoods and records none in 15. Five Points holds 2,757 restricted units, the most of any neighborhood. 2,628 units are supportive units, all of them in rental projects.

Part of Machine Readable: https://adowlen.github.io/machine-readable/

## Contents

- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit record, methods checklist, sync gate
- reviewer-notes.md - claims most likely challenged, checks not completed, flags
- sources.md - dataset citations
- social-drafts.md - LinkedIn draft (held for a Friday synthesis under the Friday-only rule)
- hero.png - hero graphic (generated illustration, headline figure composited; code/hero_composite.py)
- charts/ - chart_top_neighborhoods.png, chart_neighborhood_rates.png, chart_decades.png
- data/ - neighborhood_panel_affordable.csv (aggregate panel), audit_output.txt, raw.json (the full source pull, published because the source is a small public inventory)
- code/ - pull_data.py, build_stats.py, audit_section10.py, charts.py, hero_composite.py

## Dependencies (match code imports)

Python 3 standard library; matplotlib (charts); Pillow (hero composite). No other third-party imports.

## Reuse and citation

Licensed CC-BY-4.0 (see LICENSE). Cite as: Machine Readable, "Denver Affordable Housing Inventory" (2026), https://github.com/adowlen/denver-affordable-housing-data-brief

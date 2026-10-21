"""Build stats.json + data/neighborhood_panel_affordable.csv from data/raw.json.
Denominator: ACS housing units by statistical neighborhood, carried from the
stack warehouse layer acs_neighborhood_units as printed in the 2026-10-19 /
2026-10-20 license briefs' neighborhood_panel.csv (acs_units column).
"""
import csv, json, pathlib, statistics
from collections import Counter, defaultdict

PKG = pathlib.Path(__file__).resolve().parent.parent
attrs = [f["attributes"] for f in json.loads((PKG / "data/raw.json").read_text())["features"]]
panel_path = PKG.parent / "denver-rental-licenses-brief-2026-10-20/data/neighborhood_panel.csv"
panel = {}
with open(panel_path) as f:
    for r in csv.DictReader(f):
        panel[r["neighborhood"]] = float(r["acs_units"])

total_units = sum(panel.values())
restricted = [a["RESTRICTED_UNITS"] for a in attrs]
supportive = [a["SUPPORTIVE_UNITS"] or 0 for a in attrs]

def agg(key):
    d = defaultdict(lambda: {"projects": 0, "restricted_units": 0, "supportive_units": 0})
    for a in attrs:
        k = a[key] if a[key] is not None else "Not determined"
        d[k]["projects"] += 1
        d[k]["restricted_units"] += a["RESTRICTED_UNITS"] or 0
        d[k]["supportive_units"] += a["SUPPORTIVE_UNITS"] or 0
    return dict(d)

neigh = agg("NEIGHBORHOOD")
neigh_rates = {}
for name, units in panel.items():
    rec = neigh.get(name, {"projects": 0, "restricted_units": 0, "supportive_units": 0})
    neigh_rates[name] = {**rec, "acs_units": units,
                         "restricted_per_1000_units": round(rec["restricted_units"] / units * 1000, 1)}
zero = sorted(n for n in panel if n not in neigh or neigh[n]["projects"] == 0)

decades = defaultdict(lambda: {"projects": 0, "restricted_units": 0})
no_date = 0
jan1 = 0
for a in attrs:
    d = a["BUILT_OPEN_DATE"]
    if not d:
        no_date += 1
        continue
    if d[5:] == "01-01":
        jan1 += 1
    dec = int(d[:4]) // 10 * 10
    decades[dec]["projects"] += 1
    decades[dec]["restricted_units"] += a["RESTRICTED_UNITS"] or 0

sizes = sorted(restricted, reverse=True)
stats = {
    "source_pull_date": "2026-10-21",
    "projects_total": len(attrs),
    "restricted_units_total": sum(restricted),
    "supportive_units_total": sum(supportive),
    "supportive_projects": sum(1 for s in supportive if s > 0),
    "supportive_share_of_restricted_pct": round(sum(supportive) / sum(restricted) * 100, 1),
    "by_status": agg("STATUS"),
    "by_rental_sale": agg("RENTAL_SALE"),
    "by_funding": agg("FUNDING_CATEGORY"),
    "funding_not_determined_projects": sum(1 for a in attrs if a["FUNDING_CATEGORY"] is None),
    "median_project_units": statistics.median(restricted),
    "largest_project_units": sizes[0],
    "top10_projects_units": sum(sizes[:10]),
    "top10_projects_share_pct": round(sum(sizes[:10]) / sum(restricted) * 100, 1),
    "projects_100plus_units": sum(1 for s in sizes if s >= 100),
    "units_in_100plus_projects": sum(s for s in sizes if s >= 100),
    "acs_housing_units_total": total_units,
    "citywide_restricted_per_1000_units": round(sum(restricted) / total_units * 1000, 1),
    "neighborhoods_total": len(panel),
    "neighborhoods_with_projects": len(panel) - len(zero),
    "neighborhoods_zero_projects": zero,
    "neighborhoods": neigh_rates,
    "top_neighborhoods_by_units": sorted(
        ((k, v["restricted_units"], v["projects"], v["restricted_per_1000_units"])
         for k, v in neigh_rates.items()), key=lambda x: -x[1])[:10],
    "by_district": agg("COUNCIL_DISTRICT"),
    "by_decade_opened": {str(k): v for k, v in sorted(decades.items())},
    "built_open_no_date": no_date,
    "built_open_jan1_placeholder_dates": jan1,
    "opened_2020_2025_projects": sum(1 for a in attrs if a["BUILT_OPEN_DATE"] and a["BUILT_OPEN_DATE"] >= "2020-01-01"),
    "opened_2020_2025_units": sum(a["RESTRICTED_UNITS"] for a in attrs if a["BUILT_OPEN_DATE"] and a["BUILT_OPEN_DATE"] >= "2020-01-01"),
    "records_no_neighborhood": sum(1 for a in attrs if not a["NEIGHBORHOOD"]),
    "records_no_address": sum(1 for a in attrs if not a["ADDRESS"]),
    "sun_valley": neigh_rates["Sun Valley"],
}
(PKG / "stats.json").write_text(json.dumps(stats, indent=2))
with open(PKG / "data/neighborhood_panel_affordable.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["neighborhood", "projects", "restricted_units", "supportive_units", "acs_units", "restricted_per_1000_units"])
    for name in sorted(neigh_rates):
        v = neigh_rates[name]
        w.writerow([name, v["projects"], v["restricted_units"], v["supportive_units"], v["acs_units"], v["restricted_per_1000_units"]])
print(json.dumps({k: stats[k] for k in ("projects_total", "restricted_units_total", "supportive_units_total", "citywide_restricted_per_1000_units")}, indent=2))
print("zero-project neighborhoods:", len(zero), zero)

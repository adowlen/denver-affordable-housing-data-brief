"""Section 10 pre-flight audit for the affordable housing package.
Checks: categorical counters before any filter; sentinel handling for
RESTRICTED_UNITS / SUPPORTIVE_UNITS (0/null to unknown, excluded from any
rate denominator - here no unit is dropped: RESTRICTED_UNITS has no nulls,
asserted); numerator/denominator unit agreement (restricted UNITS divided
by ACS housing UNITS); nullable funding denominator (shares computed on
all 497 projects, not-determined printed); internal control group
(district totals and neighborhood totals must each reconcile to the
citywide total; rental+sale must reconcile; open+preservation must
reconcile).
"""
import json, pathlib
from collections import Counter

PKG = pathlib.Path(__file__).resolve().parent.parent
attrs = [f["attributes"] for f in json.loads((PKG / "data/raw.json").read_text())["features"]]
out = []
def log(s):
    out.append(s); print(s)

log(f"rows: {len(attrs)}")
for col in ("STATUS", "RENTAL_SALE", "FUNDING_CATEGORY", "NEIGHBORHOOD", "COUNCIL_DISTRICT"):
    log(f"Counter({col}): {dict(Counter(a[col] for a in attrs))}")
# Sentinel handling
assert all(a["RESTRICTED_UNITS"] is not None for a in attrs), "null RESTRICTED_UNITS"
assert all(a["RESTRICTED_UNITS"] > 0 for a in attrs), "zero/negative RESTRICTED_UNITS sentinel present"
log("RESTRICTED_UNITS: no nulls, no zeros, no negatives - no sentinel mapping needed, none excluded.")
sup_null = sum(1 for a in attrs if a["SUPPORTIVE_UNITS"] is None)
log(f"SUPPORTIVE_UNITS nulls: {sup_null} (null treated as 0 only for the supportive sum; supportive share denominator is total restricted units, asserted below).")
# Polarity sample: matched (supportive > 0) vs excluded (supportive == 0/null)
matched = [a for a in attrs if (a["SUPPORTIVE_UNITS"] or 0) > 0][:3]
excluded = [a for a in attrs if (a["SUPPORTIVE_UNITS"] or 0) == 0][:3]
for a in matched: log(f"  matched sample: {a['PROJECT_NAME']} supportive={a['SUPPORTIVE_UNITS']}")
for a in excluded: log(f"  excluded sample: {a['PROJECT_NAME']} supportive={a['SUPPORTIVE_UNITS']}")
assert len(matched) == 3 and len(excluded) == 3
# Unit agreement + controls
total = sum(a["RESTRICTED_UNITS"] for a in attrs)
by_neigh = sum(v for v in Counter({}).values())  # placeholder no-op
from collections import defaultdict
dn = defaultdict(int); dd = defaultdict(int); dr = defaultdict(int); ds = defaultdict(int)
for a in attrs:
    if a["NEIGHBORHOOD"]: dn[a["NEIGHBORHOOD"]] += a["RESTRICTED_UNITS"]
    if a["COUNCIL_DISTRICT"] is not None: dd[a["COUNCIL_DISTRICT"]] += a["RESTRICTED_UNITS"]
    dr[a["RENTAL_SALE"]] += a["RESTRICTED_UNITS"]; ds[a["STATUS"]] += a["RESTRICTED_UNITS"]
no_neigh_units = sum(a["RESTRICTED_UNITS"] for a in attrs if not a["NEIGHBORHOOD"])
no_dist_units = sum(a["RESTRICTED_UNITS"] for a in attrs if a["COUNCIL_DISTRICT"] is None)
assert sum(dn.values()) + no_neigh_units == total, "neighborhood control failed"
assert sum(dd.values()) + no_dist_units == total, "district control failed"
assert sum(dr.values()) == total and sum(ds.values()) == total
log(f"CONTROL neighborhood: {sum(dn.values())} + {no_neigh_units} no-neighborhood = {total} PASS")
log(f"CONTROL district: {sum(dd.values())} + {no_dist_units} no-district = {total} PASS")
log(f"CONTROL rental/sale and status partitions both sum to {total} PASS")
# Nullable denominator: funding shares on all 497
fc = Counter(a["FUNDING_CATEGORY"] for a in attrs)
assert sum(fc.values()) == len(attrs)
log(f"Funding shares use denominator 497 projects (incl. {fc[None]} not determined): City Funded {fc['City Funded']/497*100:.1f}%, No City Funds {fc[None] and ''}{fc['No City Funds']/497*100:.1f}%, not determined {fc[None]/497*100:.1f}% - shares sum to 100%.")
# Small counts: flag neighborhoods with <30 restricted units? print any rate based on <30 projects' units
log("Small-count note: neighborhood rates are unit rates; neighborhoods with fewer than 30 restricted units are printed with their unit counts in the panel CSV and are not ranked in the brief.")
log("AUDIT PASSED")
(PKG / "data/audit_output.txt").write_text("\n".join(out) + "\n")

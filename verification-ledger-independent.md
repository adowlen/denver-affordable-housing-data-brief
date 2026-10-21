# Independent Verification Ledger — Denver Income-Restricted Affordable Housing Brief (2026-10-21)

Independent verification pass, run 2026-10-21. This ledger was produced by a
verifier who did NOT read or reuse any builder code. At the time of this pass
the package contained only the raw pull — no builder `stats.json`, brief,
charts, or build script existed to check against — so the figures below are
the independently recomputed ground truth the builder's package must tie to.
All figures were recomputed with a fresh, separately written implementation
(scratch Python in this run, not saved into the package `code/` folder)
reading only:

- Raw snapshot: `data/raw.json` in this package — ArcGIS FeatureServer
  response for HOST_AFFORDABLEHOUSING, 497 features, fields PROJECT_NAME,
  ADDRESS, STATUS, BUILT_OPEN_DATE, PRESERVED_DATE, RESTRICTED_UNITS,
  SUPPORTIVE_UNITS, RENTAL_SALE, FUNDING_CATEGORY, NEIGHBORHOOD,
  COUNCIL_DISTRICT, LONG, LAT, FID.
- Neighborhood denominator panel:
  `../denver-rental-licenses-brief-2026-10-20/data/neighborhood_panel.csv`
  (78 rows; `acs_units` column). Per that package's Methods, `acs_units` is
  ACS 2020–2024 5-year table B25001 total housing units at tract level for
  Denver County (359,581 units countywide), allocated to the 78 statistical
  neighborhoods in proportion to tract area inside each neighborhood polygon
  (359,351.5 units allocated). It is a total-housing-units denominator —
  owner-occupied and vacant units included — NOT a renter-occupied or
  low-income-household denominator.

Verdict language: because no builder figures existed yet, no figure here is
marked reproduced / corrected / refuted against a claim. Every figure is
stated as **recomputed**; the builder must match it at printed precision or
explain the difference in the package verification file.

## Headline recomputed figures

| # | Figure | Recomputed | Notes |
|---|--------|------------|-------|
| 1 | Total projects (features) | 497 | FID 1–497, contiguous, no missing FIDs, no duplicate PROJECT_NAME values |
| 2 | RESTRICTED_UNITS sum | 29,474 | No nulls, no zeros, no negatives; min 1, max 476, mean 59.3, median 41 per project |
| 3 | SUPPORTIVE_UNITS sum | 2,628 | No nulls; 438 projects carry 0; only 59 projects carry any supportive units |
| 4 | Supportive share of restricted | 8.92% (2,628 / 29,474 = 0.08916) | Ratio, not a clean subset share — see Trap 6 (Warren Village 94 supportive > 93 restricted) |
| 5 | Restricted units, neighborhood-assigned only | 29,389 | 29,474 minus 85 units on the 2 records with no neighborhood (Trap 5) |
| 6 | Citywide restricted per 1,000 ACS units | 82.0 per 1,000 (29,474 / 359,351.5 × 1,000 = 82.02) | Numerator includes the 85 unassigned units. On assigned units only: 81.8 per 1,000 (29,389 / 359,351.5 × 1,000 = 81.78). The brief must state which numerator it uses; do not mix them in one figure |
| 7 | Sun Valley restricted rate | 2,378.2 per 1,000 ACS units (1,196 / 502.9 × 1,000) | 29.0× the citywide 82.0 rate. Sun Valley holds 4.06% of city restricted units on 0.14% of city ACS housing units — a very small denominator (502.9 units); print the underlying counts with the rate |
| 8 | Neighborhoods with zero projects | 15 of 78 panel neighborhoods | List in the neighborhood section below; they hold 47,958.7 ACS units, 13.3% of the allocated city total |
| 9 | Neighborhoods with at least 1 project | 63 of 78 | Plus 2 projects (85 units) with no neighborhood at all |

## Breakdowns

### By STATUS (Counter over all unique values — only 2 exist)

| STATUS | Projects | Restricted units | Supportive units | Share of restricted |
|--------|----------|------------------|------------------|---------------------|
| Constructed & Open | 494 | 29,299 | 2,628 | 99.41% |
| Preservation in Progress | 3 | 175 | 0 | 0.59% |
| Total | 497 | 29,474 | 2,628 | 100% |

The 3 Preservation in Progress records are Barth Hotel (62, Union Station),
Denver Dry Goods (preserved units) (51, CBD), and ECLT Scattered Sites
(62, no neighborhood). **The headline 29,474 is not an "open / existing
supply" total** — it includes these 175 not-yet-(re)opened units. If the
brief calls anything "open," the defensible total is 29,299.

### By RENTAL_SALE (Counter over all unique values — only 2 exist)

| RENTAL_SALE | Projects | Restricted units | Supportive units | Share of restricted |
|-------------|----------|------------------|------------------|---------------------|
| Rental | 401 | 26,907 | 2,628 | 91.29% |
| Sale | 96 | 2,567 | 0 | 8.71% |
| Total | 497 | 29,474 | 2,628 | 100% |

Sale units are income-restricted for-sale (ownership) homes, not rental
supply. Any sentence about rental supply must use 26,907, not 29,474. All
supportive units are in Rental projects. See Trap 3 for the single Sale
record that dominates this category.

### By FUNDING_CATEGORY (Counter over all unique values — 3, including null)

| FUNDING_CATEGORY | Projects | Restricted units | Supportive units | Share of restricted |
|------------------|----------|------------------|------------------|---------------------|
| City Funded | 256 | 15,635 | 2,483 | 53.05% |
| No City Funds | 237 | 13,658 | 145 | 46.34% |
| (null) | 4 | 181 | 0 | 0.61% |
| Total | 497 | 29,474 | 2,628 | 100% |

The 4 null-funding records (181 units) are Ash Apartments (53, Baker),
Maple Apartments (83, Cole), La Alma Family (34, Lincoln Park), and Habitat
High Street Preservation (11, Cole); all 4 also carry a null
BUILT_OPEN_DATE. Supportive units are concentrated in City Funded projects:
2,483 of 2,628 (94.5%). "No City Funds" means only that — no city funds in
this dataset's categorization. The dataset carries no federal, state,
LIHTC, or private funding field, so "No City Funds" must never be rendered
as "unsubsidized," "privately funded," or "market" (Trap 7).

## Neighborhoods

### Top 5 by restricted units (as recorded, neighborhood field as-is)

| Rank | Neighborhood | Projects | Restricted units | Supportive units | Rate per 1,000 ACS units |
|------|--------------|----------|------------------|------------------|--------------------------|
| 1 | Five Points | 56 | 2,757 | 457 | 176.2 (15,648.5 ACS units) |
| 2 | Central Park | 33 | 1,998 | 91 | 159.0 (12,563.2 ACS units) |
| 3 | Lincoln Park | 22 | 1,740 | 0 | 424.9 (4,094.6 ACS units) |
| 4 | West Colfax | 17 | 1,621 | 94 | 225.6 (7,186.2 ACS units) |
| 5 | Ruby Hill | 10 | 1,303 | 85 | 353.2 (3,689.1 ACS units) |

Top 5 together: 138 projects, 9,419 restricted units, 32.0% of the city
total. Next, for context: Sun Valley 1,196 (10 projects, 6th), Westwood
1,009 (17), Capitol Hill 990 (23), Northeast Park Hill 979 (17), North
Capitol Hill 934 (12). Gateway - Green Valley Ranch and East Colfax tie at
804.

**This ranking is not robust to the dispersed-portfolio trap (Trap 2).**
Removing only the 3 DHA Dispersed Housing records changes the top 5 to
Five Points 2,757; Central Park 1,998; West Colfax 1,621; Lincoln Park
1,417; Sun Valley 1,196 — Ruby Hill falls to 884 (10th) and Sun Valley
enters the top 5. The brief must either keep the as-recorded ranking with
the dispersed-portfolio caveat printed next to it, or not present the
ranking as a ranking of place-based supply.

### Join to the neighborhood panel

- Panel neighborhoods: 78. Raw-data named neighborhoods: 63 distinct.
- Name match: all 63 named raw neighborhoods match a panel neighborhood
  exactly (100% of named values; no spelling variants found). The only
  unmatched records are the 2 with a null NEIGHBORHOOD (Trap 5), not a
  name-matching failure. Record-level assignment rate: 495 / 497 = 99.6%.
- Panel ACS total: 359,351.5 units (sum of `acs_units`).
- Zero-project neighborhoods (15): Auraria (107.2 ACS units), Barnum West
  (1,965.0), Belcaro (3,365.9), Cory - Merrill (1,812.6), Country Club
  (1,485.7), Goldsmith (3,001.2), Hilltop (3,850.2), Indian Creek (2,165.0),
  Kennedy (2,271.0), Marston (5,597.2), North Park Hill (4,481.3),
  Southmoor Park (3,954.1), Washington Park (3,770.8), Wellshire (1,432.2),
  Windsor (8,699.3). Combined ACS units 47,958.7.
- "Zero projects" means zero records in this HOST inventory assigned to
  that neighborhood — in the data as recorded. Because dispersed and
  scattered-site portfolios are booked to a single neighborhood (Trap 2),
  a "zero" neighborhood may in fact contain individual scattered-site
  homes from those portfolios that the dataset does not locate there. The
  brief must phrase zeros as "no projects recorded in this inventory for
  [neighborhood]," never as "no income-restricted homes in [neighborhood]."
  Auraria's denominator is also institutionally dominated (107.2 ACS
  units), so its zero is not comparable to a residential neighborhood's.

### Sun Valley

10 projects, 1,196 restricted units, 0 supportive units, 502.9 ACS units,
2,378.2 restricted per 1,000 ACS units — by far the highest rate in the
city (next: Lincoln Park 424.9, Ruby Hill 353.2, Globeville 280.7,
Northeast Park Hill 279.3). Largest Sun Valley record: Sun Valley Homes,
324 units. The rate is arithmetically correct and the denominator is
unusually small; per the methods standards, print "1,196 units against
502.9 ACS housing units" alongside any per-1,000 figure, and note that the
ACS denominator is total housing units, so a rate above 1,000 per 1,000 is
possible in a neighborhood where restricted homes are a large share of a
small, redeveloping housing stock — it is not an error and not a share.

## Adversarial documentation check — semantic traps

### Trap 1 — "Project" is a record grain, not a building or a site

497 counts dataset records. It mixes single buildings, phased townhome
groups (e.g. Park Hill Village Phases I–VI booked as 5 separate records at
the same 4100 Albion St address area, 11 units combined), scattered-site
portfolios (Trap 2), and at least one apparent subdivision-scale aggregate
(Trap 3). Mean 59.3 and median 41 units per record; 97 records carry 10 or
fewer units (508 units combined); 20 records carry 200 or more (5,471
units combined). Never call 497 "buildings," "developments on 497 sites,"
or "properties" without the grain caveat.

### Trap 2 — Dispersed / scattered portfolios booked to one neighborhood (material to rankings, rates, and the map)

Three Denver Housing Authority dispersed portfolios are each a single
record, at a single address / point, in a single neighborhood:

| Record | Booked to | Address on record | Restricted units |
|--------|-----------|-------------------|------------------|
| DHA Dispersed Housing South | Ruby Hill | 2945 W Florida Ave | 419 |
| DHA Dispersed Housing East | Montbello | 5040 Paris St | 340 |
| DHA Dispersed Housing West | Lincoln Park | 1550 W Colfax Ave | 323 |

Combined 1,082 units, 3.67% of all restricted units in the city. By the
records' own names these units are dispersed; the dataset gives no
unit-level locations, so their true neighborhood distribution cannot be
recovered from this source. Effects if taken at face value:

- Ruby Hill: 1,303 recorded, 884 without DHA South. DHA South alone is
  32.2% of Ruby Hill's recorded total and is what puts Ruby Hill in the
  top 5 (see sensitivity above).
- Lincoln Park: 1,740 recorded, 1,417 without DHA West.
- Montbello: 764 recorded, 424 without DHA East — its recorded total
  nearly halves.
- Their rates per 1,000 ACS units inherit the same distortion.

The same pattern, smaller, recurs in at least 6 more records — West Denver
Scattered Sites (6 units, address literally "MULTIPLE NEIGHBORHOODS,"
booked to Barnum), Lincoln Park - Scattered Sites (57), GAO Homes -
Scattered Sites (44, West Colfax), Habitat for Humanity (Scattered Site)
(33, CBD) and Habitat Scattered Site Acquisition (24, CBD) — both Habitat
records carry the address "201 W Colfax Ave," an administrative-looking
address, not a housing site — and ECLT Scattered Sites (62, no
neighborhood at all). Dispersed + explicitly scattered records together:
1,308 units. Any map that plots these records as points, and any
neighborhood ranking, rate, or "zero" claim, carries this distortion; the
brief must disclose it in Methods and next to the ranking, and the map /
chart must not present a dispersed portfolio's point as the location of
its units.

### Trap 3 — Green Valley Ranch: the largest "project" in the dataset is a Sale aggregate with no address

"Green Valley Ranch" (FID 325): 476 restricted units — the single largest
record in the dataset — RENTAL_SALE = Sale, FUNDING_CATEGORY = No City
Funds, ADDRESS = null, BUILT_OPEN_DATE = 2003-01-01 (a Jan-1 date, see
Trap 4), booked to Gateway - Green Valley Ranch. It reads as an aggregate
tally for a subdivision / program area, not one building or one site; the
dataset provides nothing to locate or subdivide it. Effects:

- It is 59.2% of Gateway - Green Valley Ranch's recorded 804 units. Without
  it the neighborhood total is 328 and its rate falls from 48.1 to 19.6
  per 1,000 ACS units (16,720.6 ACS units).
- It is 18.5% of all Sale restricted units. Without it, Sale falls from
  2,567 to 2,091 and the Sale share of the city total falls from 8.71%
  to 7.21% (2,091 / 28,998).
- It must never be described as "Denver's largest affordable housing
  project / building / development" without the aggregate, for-sale,
  no-address qualification printed with the claim. A chart of "largest
  projects" that bars it against single buildings juxtaposes different
  record grains without a label — not permitted under the framing
  standard.

Related coordinate caution in the same neighborhood: at least 3 other
Gateway - Green Valley Ranch records carry LONG / LAT points far from
their stated addresses (e.g. Trails at Parkfield Lake, "5255 N Memphis
St," plots at -105.0419, 39.70434 in south-central Denver; Redstone Ranch
I and III, "4775 Argonne St," plot near -104.97, 39.74). Do not build a
map from LONG / LAT without a coordinate-vs-address sanity check.

### Trap 4 — BUILT_OPEN_DATE is year-grade for a third of records; do not do finer time analysis

- Non-null dates: 490 of 497; null: 7.
- Dated exactly January 1: 163 records — 33.3% of dated records, 32.8% of
  all records. Dated the 1st of any month: 226 of 490 (46.1%).
- The defensible reading is that Jan-1 dates encode a known year and an
  unknown month/day (year-only dates rendered as YYYY-01-01 by the
  DateOnly field), and day-01 dates generally are at best month-grade.
  The brief may use BUILT_OPEN_DATE by year / decade only; it must not
  report openings by month, quarter, season, or exact date, and must not
  compute ages or "opened on" dates for Jan-1 records.
- Three records are dated 1900-01-01 (Olive Street, Montclair; Pine
  Apartments, Five Points; Poplar Street, Washington Virginia Vale) —
  a placeholder / unknown pattern, not a verified 1900 opening. Year
  range as recorded is 1900–2025 across 77 distinct years; by decade:
  1900s 9, 1910s 3, 1920s 2, 1930s 1, 1940s 3, 1950s 10, 1960s 14,
  1970s 15, 1980s 23, 1990s 52, 2000s 137, 2010s 127, 2020s 94.
- PRESERVED_DATE is populated on only 24 records (473 null); a null
  preserved date cannot be read as "never preserved."

### Trap 5 — Two records have no neighborhood and no council district (85 units excluded from every neighborhood figure)

| Record | Units | Details |
|--------|-------|---------|
| Xenia Street Apartments, 1371 N Xenia St (FID 245) | 23 | Rental, No City Funds, Constructed & Open, dated 2024-12-01 |
| ECLT Scattered Sites (FID 287) | 62 | Sale, City Funded, Preservation in Progress, no address, no BUILT_OPEN_DATE |

Together 85 restricted units (0.29% of the city total). They are in the
city totals (29,474) and in the STATUS / RENTAL_SALE / FUNDING_CATEGORY
breakdowns, and out of every neighborhood count, sum, ranking, and rate.
Neighborhood sums therefore reconcile to 29,389, not 29,474 — the brief's
methods must state this reconciliation explicitly so the gap does not read
as an error. Council-district sums reconcile the same way (districts on
495 records: D9 107 projects, D10 92, D3 77, D8 64, D1 41, D7 37, D5 25,
D2 18, D6 12, D4 11, D11 11, null 2).

### Trap 6 — SUPPORTIVE_UNITS is not a strict subset in the data as recorded

Warren Village (Cheesman Park) records 94 supportive units against 93
restricted units — the one record where supportive exceeds restricted.
Every other record satisfies supportive ≤ restricted, and there are no
nulls in either field. So 8.92% is "supportive units as a ratio to
restricted units," and the brief must not claim every supportive unit is
counted inside the restricted total, nor recompute a "non-supportive
restricted" remainder (29,474 − 2,628 = 26,846) as an exact figure without
flagging this 1-unit inconsistency. It is immaterial to any headline
number and material to exact-subset wording.

### Trap 7 — Category labels mean only what the dataset means

- STATUS has exactly 2 values (above). There is no "under construction,"
  "planned," or "closed / expired" category in this pull — the brief
  cannot speak to pipeline or to restrictions that have expired.
- FUNDING_CATEGORY has exactly 2 non-null values plus null (above). No
  inference about total public subsidy, LIHTC status, or affordability
  level (AMI band) is supported: the dataset carries no AMI, rent, income,
  affordability-period, or expiration field at all. Any claim about who
  the units are affordable *to*, or for how long, is outside this source.
- RESTRICTED_UNITS is taken as the dataset's count of income-restricted
  units per record. The dataset does not state whether a record's total
  unit count exceeds its restricted count, so no "share of the project
  that is restricted" and no total-project-size figure can be derived.
- ADDRESS is null on 19 records, including the largest record (Trap 3)
  and ECLT Scattered Sites; 7 non-null addresses are shared by 2 or more
  records (4100 Albion St appears on 5 — the Park Hill Village phases).
  Address is not a unique key and cannot be used to deduplicate.

### Trap 8 — Denominator scope for every per-1,000 rate

Rates in this ledger divide restricted *units* (a stock in this inventory)
by ACS *total housing units* allocated to the neighborhood. That is an
exposure rate, not a share of rental stock, not a share of low-income
households, and not a needs-coverage measure; the panel carries no
renter-occupied or income-qualified denominator (the same limitation the
2026-10-20 rental-licenses brief recorded). Labels on every chart and in
every sentence must read "restricted units per 1,000 housing units (ACS
2020–2024 5-year, B25001, allocated)" or equivalent — never "% affordable,"
"share of rentals," or "coverage." Citywide 82.0 and Sun Valley 2,378.2
are comparable to each other (same numerator source, same denominator
basis) and to nothing that uses a different denominator.

## Methods checklist items this pass can and cannot close

- Zero / null sentinels: RESTRICTED_UNITS and SUPPORTIVE_UNITS have no
  nulls, zeros are real recorded values only for SUPPORTIVE_UNITS (438
  records); no sentinel filtering was needed or applied. FUNDING_CATEGORY
  nulls (4) and NEIGHBORHOOD / COUNCIL_DISTRICT nulls (2) are counted and
  shown above, never silently dropped.
- Join match rate: neighborhood-to-panel join matches 63 / 63 named
  neighborhoods (100%); 495 / 497 records (99.6%) carry a neighborhood.
  The 2 unmatched records are null-key records, not failed matches, and
  there is no evidence they differ systematically beyond being one
  ordinary apartment record and one scattered-site portfolio (Trap 5).
- Small counts: rates for neighborhoods with small ACS denominators
  (Sun Valley 502.9, Auraria 107.2) must carry their underlying counts.
- Category / definition change over time: cannot be checked from this
  single snapshot — the dataset is a current inventory with a
  BUILT_OPEN_DATE field, not a time series, and carries no vintage or
  revision field. Any trend sentence would need a second dated pull.
- Causality / exposure: rates use the exposure denominator above; no
  causal reading is supported by this source alone.

## Bottom line for the builder

All assigned figures recompute cleanly and are stated above at full
precision. There is no arithmetic blocker. There are three wording /
framing blockers the package must satisfy before publication:

1. The top-5 neighborhood ranking and every neighborhood rate must carry
   the dispersed-portfolio caveat (Trap 2), and the "zero neighborhoods"
   claim must be phrased as "no projects recorded in this inventory."
2. The Green Valley Ranch 476-unit Sale record must never be presented
   as a single building / largest project without its aggregate,
   for-sale, no-address qualification (Trap 3), and Rental vs Sale and
   Open vs Preservation in Progress must not be collapsed in any
   "rental supply" or "open supply" sentence.
3. BUILT_OPEN_DATE may be used by year only (Trap 4), and every
   per-1,000 rate must be labeled with the ACS total-housing-units
   denominator (Trap 8), with Sun Valley's counts printed beside its rate.

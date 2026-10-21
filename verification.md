# Verification - Denver Affordable Housing Inventory brief (2026-10-21)

## Pre-flight audit (Section 10)

Audit script: code/audit_section10.py. Full output: data/audit_output.txt. Result: AUDIT PASSED.

- Zero/null sentinel handling: RESTRICTED_UNITS has no nulls, zeros, or negatives in the 497-row pull (asserted); no sentinel mapping was needed and no record was excluded from any total. SUPPORTIVE_UNITS has no nulls. "Unknown" categories are therefore absent from unit totals; the one nullable categorical used for shares, FUNDING_CATEGORY, is handled under the nullable-denominator check below.
- Sentinel polarity sample: supportive filter (SUPPORTIVE_UNITS > 0) matched vs excluded 3-row samples are printed in data/audit_output.txt (matched: 10th & Sheridan 60, 1467 N Detroit St. - Empowerment Program 4, 17th Street Redevelopment 36; excluded: three projects with 0). The inequality matches the intended meaning: matched rows carry supportive units, excluded rows carry none.
- Numerator/denominator unit agreement: every rate divides restricted UNITS by ACS housing UNITS; every share divides units by units or projects by projects. No rate mixes projects with units.
- Categorical exhaustiveness: Counters for every column used in a filter or grouping are printed in data/audit_output.txt before filtering: STATUS (Constructed & Open 494, Preservation in Progress 3 - no other values exist), RENTAL_SALE (Rental 401, Sale 96), FUNDING_CATEGORY (City Funded 256, No City Funds 237, None 4), plus full NEIGHBORHOOD and COUNCIL_DISTRICT counters.
- Nullable-denominator trap: funding shares are computed on all 497 projects; the 4 not-determined projects (0.8 percent) are printed in the brief and the shares sum to 100 percent on the full denominator.
- Join hygiene: no spatial or relational join is performed in this package. Neighborhood and district are fields carried in the source itself. The one cross-source operation is the rate denominator (ACS units by neighborhood name, exact name match against the 78-neighborhood panel): all 63 neighborhoods named in the inventory match a panel name; the 2 records with no neighborhood in the source are counted citywide only. Physical scale is printed beside every rate: restricted units and ACS housing units both appear in the panel data file.
- Internal control group (Section 10.2): two independent partitions of the same total reconcile exactly - neighborhood sums (29,389) plus the 85 units on records with no neighborhood equal 29,474; district sums (29,389) plus the same 85 equal 29,474; rental/sale and status partitions each sum to 29,474. PASS, printed in data/audit_output.txt.

## Sync gate (Section 10.3)

- README dependency list matches code imports: Python standard library, matplotlib, and Pillow only; the README lists exactly those.
- Every number in brief-draft.md was cross-checked against stats.json after the final build_stats.py run (29,474; 497; 2,628; 8.9 percent; 26,907; 2,567; 82.0; 15 zero neighborhoods by name; Five Points 2,757/56; Central Park 1,998/33; Lincoln Park 1,740/22 and 424.9; Ruby Hill 353.2; Globeville 280.7; Northeast Park Hill 279.3; West Colfax 225.6; Sun Valley 1,196/10 and ACS base 502.9; median 41; 87 projects at 100+ units holding 14,430; top 10 projects 3,320 (11.3 percent); decades 7,350 / 7,169 / 6,270; pre-2000 8,331; Jan-1 dates 163 of 490 dated; 7 undated; funding 256/15,635, 237/13,658, 4/181; supportive by funding 2,483 / 145; District 10 supportive 839, District 9 772, Districts 4 and 11 zero). PASS.

## Methods checklist (standards Section 3)

- Base rates and exposure: rates per 1,000 ACS housing units are used for every neighborhood comparison; raw counts are always printed beside rates. Exposure limit: the ACS base and the 2026 inventory have different vintages; Sun Valley's restricted count exceeds its ACS base, and the brief prints that break explicitly and does not rank Sun Valley's rate.
- Direction of causality: no causal claim is made; the brief describes the current map and the What this might mean section carries the strongest alternative (historical land cost and zoning at opening date) beside the stock-pattern reading.
- Category and definition changes: the inventory is a single snapshot (service layer dated 20250930), so no within-window category change applies. BUILT_OPEN_DATE decade grouping is descriptive of the standing inventory, not a construction time series: projects that closed or left restriction are not in this inventory, and the brief does not present decade counts as production counts.
- Exact date range: source pulled October 21, 2026; project open dates as filed run 1900-2025; the Denver 2027 budget dates are confirmed in effect for the Who can act section (Council release, denvergov.org, 2026-10-09).
- Joins: no dataset join; neighborhood-name denominator match rate is 63 of 63 named neighborhoods (100 percent); 2 of 497 records (0.4 percent) carry no neighborhood and are handled as printed.
- Small numbers: neighborhood rates are printed with unit counts; neighborhoods with very small restricted counts (for example Montclair, 5 units; Platt Park, 4 units) are not ranked or headlined, and their counts appear in the panel data file.
- Official definitions: "income-restricted" and the field names are HOST's own as published in the inventory; the brief uses them as filed and notes the inventory carries no AMI band field.
- Layering admission test: the ACS neighborhood-units layer is admitted for one claim the brief could not make without it - restricted units per 1,000 housing units by neighborhood (Finding 3). The STR and rental register layers were considered and cut: no claim in this brief requires them, and the cut is recorded here.

## Section 11 status

- Builder pass: this package (built in the 2026-10-21 morning run; no overnight package existed).
- Independent verifier: dispatched as a separate pass recomputing from data/raw.json with a separate implementation; its ledger is verification-ledger-independent.md in this package. Figures in the brief were held to the builder's stats.json values; any verifier discrepancy is recorded in reviewer-notes.md.
- Adversarial pass: the verifier pass was also briefed on semantic traps (dispersed portfolios, the Green Valley Ranch Sale row, Jan-1 placeholder dates, the 2 unlocated records); its findings are adjudicated in reviewer-notes.md.
- Publication gate: under Alex's 2026-10-20 rule, publication is pre-authorized when QA and audit gates pass. Section 11 completeness is assessed in reviewer-notes.md; if the independent ledger has not landed or carries an open discrepancy at report time, the package is HELD and that is the blocking reason.

## Section 11 fix loop (2026-10-21, adjudicated from the full text of verification-ledger-independent.md)

The independent verifier recomputed every assigned figure with a separate implementation and matched the builder's stats.json on all of them (497 projects; 29,474 restricted; 2,628 supportive; 82.0 citywide; Sun Valley 2,378.2 with counts; top-5 neighborhoods; 15 zero-project neighborhoods; all status / rental-sale / funding partitions; decade counts; join match 63 of 63 named neighborhoods). No arithmetic discrepancy. Its three framing blockers, each adjudicated and fixed in the brief text:

1. Dispersed portfolios (ledger Trap 2): count CORRECT (3 DHA records, 1,082 units; 1,308 with scattered sites), mechanism CORRECT (booked to one neighborhood each), treatment APPLIED: Finding 4 now names all three DHA portfolios and prints the without-dispersed totals for Ruby Hill (884), Lincoln Park (1,417), and Montbello (424); the lead paragraph and the social draft now phrase zeros as "records no project in this inventory," with the scattered-site caveat in the same paragraph; the hero line was recomposited to "15 of 78 neighborhoods: none listed" over the inventory source line.
2. Green Valley Ranch aggregate (Trap 3): count CORRECT (476, Sale, no address, 59.2 percent of its neighborhood's recorded total), treatment APPLIED: Finding 4 prints the aggregate, for-sale, no-address qualification and the without-it neighborhood total (328); no chart in this package bars largest projects, so no mixed-grain graphic exists.
3. Date resolution and rate labels (Traps 4 and 8): the brief already grouped by decade only; the 1900-01-01 placeholder pattern (3 records) is now printed in Finding 5. Every rate in the brief and charts is labeled per 1,000 housing units (ACS); Sun Valley's counts are printed beside any mention of its rate and it is excluded from the ranked rate chart with the reason on the chart.

Additional verifier traps adjudicated: Trap 5 (2 unlocated records, 85 units) - reconciliation now printed in Data notes, including that the citywide 82.0 uses the full numerator and assigned-only would be 81.8. Trap 6 (Warren Village supportive 94 vs restricted 93) - Finding 2 now prints supportive as a ratio, not a subset. Trap 7 (category scope) - the brief already makes no pipeline, subsidy, or AMI claim; "No City Funds" is used only as the filed label. Trap 1 (record grain) - Finding 4. Coordinate caution (Trap 3 note): this package builds no map from LONG/LAT, so the misplotted Gateway coordinates cannot enter any graphic.

Section 11 status after the fix loop: builder, Section 10 gates, independent verifier, and adversarial documentation check all complete; all verifier findings have dispositions above. No open finding.

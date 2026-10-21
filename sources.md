# Sources - Denver Affordable Housing Inventory brief (2026-10-21)

Primary source (all project and unit figures):
- Denver Department of Housing Stability (HOST) Affordable Housing Inventory, HOST_AFFORDABLEHOUSING, Denver Open Data Catalog, ArcGIS FeatureServer layer 0 at services1.arcgis.com/zdB7qR0BtYrg0Xpl. Pulled in full October 21, 2026 via code/pull_data.py: 497 features. Service layer name as served: HOST_AFFORDABLEHOUSING_20250930. Fields used: PROJECT_NAME, ADDRESS, STATUS, BUILT_OPEN_DATE, PRESERVED_DATE, RESTRICTED_UNITS, SUPPORTIVE_UNITS, RENTAL_SALE, FUNDING_CATEGORY, NEIGHBORHOOD, COUNCIL_DISTRICT, LONG, LAT, FID.
- Figures: 497 projects; 29,474 RESTRICTED_UNITS summed as filed; 2,628 SUPPORTIVE_UNITS summed as filed; all status, rental/sale, funding, neighborhood, district, and decade groupings computed from this pull by code/build_stats.py and recorded in stats.json.

Denominator source (rates only):
- ACS housing units by Denver statistical neighborhood (acs_units), from the Machine Readable stack warehouse layer acs_neighborhood_units, as carried in the neighborhood panel of the Denver STR licenses brief (2026-10-19) and Denver rental licenses brief (2026-10-20): ACS 2020-2024 5-year table B25001 total housing units (owner, renter, and vacant units all included - not a renter or low-income denominator), 359,581 units county-wide at tract level, allocated to the 78 statistical neighborhoods in proportion to tract area inside each neighborhood polygon: 359,351.5 units allocated, 229.5 county units unallocated, and the fractional values are area-allocation artifacts. Rates in the brief use the allocated values as carried. Derived figures (labeled derived in the brief): every per-1,000 rate, every percentage share, the 49.0 percent share of units in projects of 100 or more units, and the pre-2000 unit sum.

Context source:
- Denver 2027 budget dates (final proposal October 19, hearing October 26, amendment vote November 2, passage November 9, 2026): Denver City Council news release on denvergov.org, published 2026-10-09, cited in this series since the 2026-10-18 traffic-accidents package and verified live that day.

No other sources. No company-reported figures are used in this brief.

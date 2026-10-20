# Île-de-France Property Market Analysis (DVF 2025)

Python + SQL + Power BI analysis of **127,033 residential property sales** across the 8 départements of Île-de-France, built on French government open data.

![Power BI dashboard](PowerBI%20dashboard.png)

## Business question
An investment firm asks: **where in Île-de-France is property most expensive per m², how do apartments compare with houses, and how did the market move during the year?**

## Data
- Source: *Demandes de valeurs foncières géolocalisées* (DVF), open data on data.gouv.fr
- Coverage: 2025 sales, départements 75, 77, 78, 91, 92, 93, 94, 95
- Raw size: 448,405 rows x 40 columns

## Method
1. Stack the 8 département files (pandas)
2. Keep apartments and houses only (drop cellars, parking, commercial premises)
3. Keep sales with exactly one home row. In DVF a sale can span several rows with the total price repeated, so multi-home deals cannot give a clean price per m²
4. Remove rows with missing price or area (49 rows)
5. Compute price per m² = sale value / built area
6. Remove implausible values outside EUR 500 - 30,000 per m² (1,352 rows)
7. Load the result into SQLite and analyse it with SQL
8. Build an interactive Power BI dashboard from the clean file

Result: **127,033 clean sales.** The headline figures (sale count, average and median price per m²) match across Python, SQL and Power BI.

## Dashboard
The Power BI report (`idf_property_dashboard.pbix`) contains:
- KPI cards: total sales, average and median price per m²
- Average price per m² by département
- Apartments vs houses inside each département
- Median price per m² by month
- Number of sales by month
- A property-type slicer that filters the whole page

## Key findings
- **Paris is the most expensive:** EUR 10,157 per m² on average, about **3.2x** Seine-et-Marne (EUR 3,168).
- Ranking by average price per m²: Paris 10,157 > Hauts-de-Seine 6,831 > Val-de-Marne 5,196 > Seine-Saint-Denis 4,350 > Yvelines 4,270 > Val-d'Oise 3,527 > Essonne 3,281 > Seine-et-Marne 3,168.
- **Simpson's paradox:** overall, apartments (EUR 6,466/m²) look much pricier than houses (EUR 4,140/m²). Inside each département the picture reverses: houses are clearly pricier per m² in 5 of 8 (Paris, Essonne, Hauts-de-Seine, Val-de-Marne, Val-d'Oise), about equal in 2 (Yvelines and Seine-Saint-Denis, within about 1%), and cheaper only in Seine-et-Marne. Apartments look pricier overall only because most of them are in Paris.
- **Seasonality in 2025:** median price per m² peaked in March (about EUR 5,167) and was lowest in August (about EUR 4,369). Sales volume peaked in July (about 15,200 sales) and was lowest in August (about 7,300).

## Assumptions and limitations
- Only single-home sales are analysed (about 93% of residential sales).
- The EUR 500 - 30,000 per m² limits are my own judgement, not an official rule.
- SQL figures are averages; the dashboard also shows medians, which are more robust to outliers.
- 2025 only, so seasonal patterns come from a single year and may not repeat, and there is no year-on-year trend yet.
- Price per m² is not adjusted for condition, floor, or exact location.

## Repository
- `01_load_data.py` - loads, cleans and filters the raw files, and saves a clean CSV
- `02_load_sql.py` - loads the clean CSV into a SQLite database (`dvf.db`)
- `03_analysis.sql` - the SQL queries behind the findings
- `idf_property_dashboard.pbix` - the Power BI report (open with Power BI Desktop)
- `dashboard.png` - screenshot of the dashboard

## How to reproduce
1. Download the 2025 DVF géolocalisées file for each of the 8 départements from data.gouv.fr and put them in one folder
2. Run `01_load_data.py` (needs Python and pandas)
3. Run `02_load_sql.py`
4. Open `dvf.db` in any SQLite tool and run the queries in `03_analysis.sql`
5. Open `idf_property_dashboard.pbix` in Power BI Desktop to explore the dashboard

## Next steps
- Commune-level price map
- Add 2024 data for a year-on-year comparison

## Tools
Python (pandas), SQLite, SQL, Power BI (DAX)

*Author: Priyanka, MSc Business Analytics, NEOMA Business School* Business School*

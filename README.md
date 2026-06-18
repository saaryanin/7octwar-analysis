# Oct 7 War Casualty Analysis

A data pipeline and Tableau visualization project analyzing casualties from the October 7, 2023 war, with a primary focus on IDF soldiers.

**Live Dashboards:**
- [Age Distribution by Role](https://public.tableau.com/app/profile/saar.yanin/viz/oct7war_analysis/AgeDistributionbyRole?publish=yes)
- [Monthly Casualties by Role](https://public.tableau.com/app/profile/saar.yanin/viz/oct7war_analysis/MonthlyCacualtiesbyRole?publish=yes)
- [IDF Soldiers Killed by Region](https://public.tableau.com/app/profile/saar.yanin/viz/oct7war_analysis/IDFSolidersKilledbyRegion?publish=yes)

---

## 1. Download the Dataset

1. Go to [oct7database.com/en.html](https://oct7database.com/en.html)
2. Scroll down to the table
3. Click **"Download full table (XLSX)"**
4. Save the file as **`oct7database_full.xlsx`** inside the `data/raw/` folder

---

## 2. Set Up the Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 3. Run the Data Pipeline

Run these three scripts in order from the project root:

```bash
# Step 1 — clean the raw XLSX and produce a CSV
python src/process_oct7data.py

# Step 2 — load the clean CSV into a SQLite database
python src/create_sqlite_db.py

# Step 3 — build the city → region lookup table (uses Nominatim geocoding)
#           seeds ~200 cities instantly, geocodes any unknowns at 1 req/sec
python src/geocode_regions.py
```

After these three steps you will have `data/oct7_analysis.db` ready.

---

## 4. Create the SQL Views (DBeaver)

This project uses [DBeaver](https://dbeaver.io/) as the SQL client.

1. Open DBeaver and connect to `data/oct7_analysis.db` (SQLite driver)
2. Open and run `sql/01_create_views.sql` — creates the four base views
3. Open and run `sql/03_tableau_views.sql` — creates the three Tableau views

> **Note:** `sql/02_statistics_queries.sql` contains exploratory queries used to generate the findings in `docs/statistics.md`. You can run them section by section to explore the data yourself.

---

## 5. Export CSVs for Tableau

```bash
python src/export_tableau_csvs.py
```

This writes three CSV files into `data/processed/`:

| File | Used for |
|---|---|
| `tableau_monthly_killed_by_type.csv` | Monthly Casualties by Role |
| `tableau_age_dist_by_role.csv` | Age Distribution by Role |
| `tableau_soldiers_by_region.csv` | IDF Soldiers Killed by Region |

---

## 6. Explore the Findings

Before opening Tableau, read **`docs/statistics.md`** for a full breakdown of the key findings — overall totals, deaths by front, age distribution, cause of death, top cities, and more. It gives you the context to understand what you are looking at in the dashboards.

---

## 7. Updating with New Data

When the source website publishes updated data, the process is the same:

1. Re-download the XLSX and replace `data/raw/oct7database_full.xlsx`
2. Re-run steps 3–5

`geocode_regions.py` skips cities it has already classified, so only genuinely new cities will hit the Nominatim API.

---

## Project Structure

```
7octwar-analysis/
├── data/
│   ├── raw/                  # Place the downloaded XLSX here
│   └── processed/            # Clean CSV + Tableau export CSVs
├── docs/
│   └── statistics.md         # Key findings and query results
├── sql/
│   ├── 01_create_views.sql   # Base views (run in DBeaver)
│   ├── 02_statistics_queries.sql  # Exploratory queries
│   └── 03_tableau_views.sql  # Tableau-optimized views (run in DBeaver)
└── src/
    ├── process_oct7data.py   # Clean raw XLSX → CSV
    ├── create_sqlite_db.py   # CSV → SQLite DB
    ├── geocode_regions.py    # Build city → region lookup table
    └── export_tableau_csvs.py  # Export views to CSV for Tableau
```

-- =============================================
-- Tableau Views — Oct 7 War Casualty Analysis
-- Connect Tableau to: data/oct7_analysis.db
-- =============================================


-- 1. MONTHLY KILLED BY ROLE
-- Use for: stacked bar chart or multi-line chart over time, colored by role
-- Tableau setup: death_year_month on Columns, count on Rows, role on Color
CREATE VIEW IF NOT EXISTS tableau_monthly_killed_by_type AS
SELECT
    CAST(SUBSTR(death_year_month, 1, 4) AS INTEGER)  AS death_year,
    CAST(SUBSTR(death_year_month, 6, 2) AS INTEGER)  AS death_month,
    role,
    COUNT(*) AS count
FROM idf_casualties
WHERE death_year_month IS NOT NULL
  AND LENGTH(death_year_month) = 7
  AND status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
  AND role IS NOT NULL
  AND role != 'Nan'
GROUP BY death_year, death_month, role
ORDER BY death_year, death_month, role;

-- 2. AGE DISTRIBUTION BY ROLE
-- Replaces the separate soldier/civilian age views.
-- Use for: bar chart with age on X axis, count on Y, role on Color
-- Tableau setup: age on Columns, count on Rows, role on Color
CREATE VIEW IF NOT EXISTS tableau_age_dist_by_role AS
SELECT
    age,
    role,
    COUNT(*) AS count
FROM idf_casualties
WHERE status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
  AND role IS NOT NULL
  AND role != 'Nan'
  AND age IS NOT NULL
GROUP BY age, role
ORDER BY age, role;

-- 3. SOLDIERS KILLED BY GEOGRAPHIC REGION
-- Regions: North (north of Hadera), Central (Hadera to Rishon Lezion + Jerusalem area),
--          South (south of Rishon Lezion to Eilat), West Bank (beyond the Green Line)
-- Requires: city_region_lookup table — run src/geocode_regions.py before creating this view.
-- Tableau setup: region on Columns, SUM(soldiers_killed) on Rows for summary bar chart;
--   add residence to detail for city-level drill-down
CREATE VIEW IF NOT EXISTS tableau_soldiers_by_region AS
WITH normalized AS (
    SELECT
        residence,
        REPLACE(REPLACE(REPLACE(residence, char(8217), char(39)),
                                            char(8216), char(39)),
                                            char(1523),  char(39)) AS res
    FROM idf_casualties
    WHERE is_soldier = TRUE
      AND status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
      AND residence IS NOT NULL
      AND residence NOT IN ('Nan', 'Unknown')
)
SELECT
    crl.region,
    n.residence,
    COUNT(*) AS soldiers_killed
FROM normalized n
INNER JOIN city_region_lookup crl ON n.res = crl.city_normalized
GROUP BY crl.region, n.residence
ORDER BY crl.region, soldiers_killed DESC;
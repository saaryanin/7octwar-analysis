-- =============================================
-- Create all useful views for 7octwar-analysis
-- =============================================

-- 1. Soldiers only view
CREATE VIEW IF NOT EXISTS soldiers AS
SELECT
    first_name,
    last_name,
    gender,
    age,
    residence,
    country,
    role,
    status_simple,
    event_date,
    death_date_clean as death_date,
    death_year,
    death_year_month,
    front,
    cause_of_death,
    event_location,
    death_location
FROM idf_casualties
WHERE is_soldier = TRUE;

-- 2. Summary by Front
CREATE VIEW IF NOT EXISTS casualties_by_front AS
SELECT
    front,
    COUNT(*) as total_casualties,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END) as soldiers,
    SUM(CASE WHEN is_soldier = FALSE THEN 1 ELSE 0 END) as civilians,
    ROUND(AVG(age), 1) as avg_age,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count,
    MIN(event_date) as first_event,
    MAX(event_date) as last_event
FROM idf_casualties
GROUP BY front
ORDER BY total_casualties DESC;

-- 3. Monthly Trends
CREATE VIEW IF NOT EXISTS monthly_casualties AS
SELECT
    death_year_month,
    front,
    COUNT(*) as total_deaths,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END) as soldiers_killed,
    COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_deaths
FROM idf_casualties
WHERE death_year_month IS NOT NULL
GROUP BY death_year_month, front
ORDER BY death_year_month;

-- 4. Status Summary
CREATE VIEW IF NOT EXISTS status_summary AS
SELECT
    status_simple,
    COUNT(*) as total,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END) as soldiers
FROM idf_casualties
GROUP BY status_simple
ORDER BY total DESC;

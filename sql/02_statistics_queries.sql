-- =============================================
-- Statistics Queries — Oct 7 War Casualty Analysis
-- Run each section in DBeaver, paste results into docs/statistics.md
-- =============================================


-- =============================================
-- 1. OVERALL TOTALS
-- =============================================

-- 1a. Grand total and soldier share
SELECT
    COUNT(*)                                                        AS total_records,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END)             AS total_soldiers,
    SUM(CASE WHEN is_soldier = FALSE THEN 1 ELSE 0 END)            AS total_civilians,
    ROUND(SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS soldier_pct
FROM idf_casualties;

-- 1b. Breakdown by status (killed / kidnapped / released / etc.)
SELECT
    status_simple,
    COUNT(*)                                                        AS total,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END)             AS soldiers,
    SUM(CASE WHEN is_soldier = FALSE THEN 1 ELSE 0 END)            AS civilians,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1)             AS pct_of_total
FROM idf_casualties
GROUP BY status_simple
ORDER BY total DESC;

-- 1c. Soldiers killed — confirmed deaths only
SELECT COUNT(*) AS soldiers_killed
FROM idf_casualties
WHERE is_soldier = TRUE
  AND status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died');


-- =============================================
-- 2. DEATHS BY FRONT
-- =============================================

-- 2a. Full breakdown per front (soldiers focus)
SELECT
    front,
    COUNT(*)                                                        AS total_casualties,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END)             AS soldiers,
    SUM(CASE WHEN is_soldier = FALSE THEN 1 ELSE 0 END)            AS civilians,
    ROUND(AVG(CASE WHEN is_soldier = TRUE THEN age END), 1)        AS avg_soldier_age,
    MIN(CASE WHEN is_soldier = TRUE THEN age END)                  AS youngest_soldier,
    MAX(CASE WHEN is_soldier = TRUE THEN age END)                  AS oldest_soldier
FROM idf_casualties
GROUP BY front
ORDER BY soldiers DESC;

-- 2b. Soldiers killed per front
SELECT
    front,
    COUNT(*)                                                        AS soldiers_killed
FROM soldiers
WHERE status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
GROUP BY front
ORDER BY soldiers_killed DESC;


-- =============================================
-- 3. MONTHLY TIMELINE
-- =============================================

-- 3a. Monthly death toll across all fronts (soldiers only)
SELECT
    death_year_month,
    COUNT(*)                                                        AS soldiers_killed
FROM soldiers
WHERE death_year_month IS NOT NULL
  AND status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
GROUP BY death_year_month
ORDER BY death_year_month;

-- 3b. Top 10 deadliest months
SELECT
    death_year_month,
    COUNT(*)                                                        AS soldiers_killed
FROM soldiers
WHERE death_year_month IS NOT NULL
  AND status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
GROUP BY death_year_month
ORDER BY soldiers_killed DESC
LIMIT 10;

-- 3c. Monthly by front (for Tableau later — useful to preview here)
SELECT *
FROM monthly_casualties
ORDER BY death_year_month, front;


-- =============================================
-- 4. AGE DISTRIBUTION OF SOLDIERS
-- =============================================

-- 4a. Summary stats
SELECT
    MIN(age)                    AS youngest,
    MAX(age)                    AS oldest,
    ROUND(AVG(age), 1)          AS avg_age,
    COUNT(age)                  AS soldiers_with_known_age,
    COUNT(*) - COUNT(age)       AS soldiers_unknown_age
FROM soldiers;

-- 4b. Age buckets
SELECT
    CASE
        WHEN age < 20            THEN 'Under 20'
        WHEN age BETWEEN 20 AND 24 THEN '20-24'
        WHEN age BETWEEN 25 AND 29 THEN '25-29'
        WHEN age BETWEEN 30 AND 34 THEN '30-34'
        WHEN age BETWEEN 35 AND 39 THEN '35-39'
        WHEN age >= 40           THEN '40+'
        ELSE 'Unknown'
    END                         AS age_group,
    COUNT(*)                    AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM soldiers
GROUP BY age_group
ORDER BY
    CASE age_group
        WHEN 'Under 20' THEN 1 WHEN '20-24' THEN 2 WHEN '25-29' THEN 3
        WHEN '30-34' THEN 4 WHEN '35-39' THEN 5 WHEN '40+' THEN 6
        ELSE 7
    END;

-- 4c. 10 youngest soldiers killed
SELECT first_name, last_name, age, front, death_date, cause_of_death
FROM soldiers
WHERE age IS NOT NULL
  AND status_simple IN ('Killed', 'Kidnapped and Killed', 'Died In Captivity', 'Released then Died')
ORDER BY age ASC
LIMIT 10;


-- =============================================
-- 5. CAUSE OF DEATH (SOLDIERS)
-- =============================================

-- 5a. Top causes overall
SELECT
    cause_of_death,
    COUNT(*)                    AS count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM soldiers
WHERE cause_of_death IS NOT NULL AND cause_of_death != 'Nan'
GROUP BY cause_of_death
ORDER BY count DESC
LIMIT 15;

-- 5b. Top cause per front
SELECT
    front,
    cause_of_death,
    COUNT(*)                    AS count
FROM soldiers
WHERE cause_of_death IS NOT NULL AND cause_of_death != 'Nan'
GROUP BY front, cause_of_death
ORDER BY front, count DESC;


-- =============================================
-- 6. RESIDENCE — WHERE DID SOLDIERS COME FROM?
-- =============================================

-- 6a. Top 20 cities/towns
SELECT
    residence,
    COUNT(*)                    AS soldiers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
FROM soldiers
WHERE residence IS NOT NULL AND residence NOT IN ('Nan', 'Unknown')
GROUP BY residence
ORDER BY soldiers DESC
LIMIT 20;

-- 6b. Foreign nationals among soldiers
SELECT
    country,
    COUNT(*)                    AS soldiers
FROM soldiers
WHERE country IS NOT NULL
  AND country NOT IN ('Nan', 'Unknown', 'Israel')
GROUP BY country
ORDER BY soldiers DESC;


-- =============================================
-- 7. GENDER BREAKDOWN
-- =============================================

SELECT
    gender,
    COUNT(*)                    AS total,
    SUM(CASE WHEN is_soldier = TRUE THEN 1 ELSE 0 END)  AS soldiers,
    SUM(CASE WHEN is_soldier = FALSE THEN 1 ELSE 0 END) AS civilians
FROM idf_casualties
WHERE gender IN ('Male', 'Female')
GROUP BY gender;

-- Female soldiers detail
SELECT first_name, last_name, age, front, role, status_simple, cause_of_death
FROM soldiers
WHERE gender = 'Female'
ORDER BY front, age;


-- =============================================
-- 8. ROLE BREAKDOWN
-- =============================================

SELECT
    role,
    COUNT(*)                    AS count,
    ROUND(AVG(age), 1)          AS avg_age
FROM soldiers
GROUP BY role
ORDER BY count DESC
LIMIT 20;

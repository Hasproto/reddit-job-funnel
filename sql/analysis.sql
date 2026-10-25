-- analysis.sql
-- Questions I asked the data and  answered with SQL.
-- Tables: posts (one row per post) and monthly_summary (one row per month).
 


-- Q1 -  How many posts are there, and how many report job search numbers?
SELECT
    COUNT(*)  AS total_posts,
    COUNT(applications)  AS posts_with_applications,
    COUNT(interviews)    AS posts_with_interviews,
    COUNT(offers)  AS posts_with_offers
FROM posts;


-- Q2 - How many posts were made each month?
SELECT
    strftime(created_at, '%Y-%m') AS month,
    COUNT(*)   AS posts
FROM posts
GROUP BY month
ORDER BY month;


-- Q3-  What percent of posts mention AI each month?
SELECT
    strftime(created_at, '%Y-%m')  AS month,
    ROUND(100.0 * AVG(CASE WHEN mentions_ai THEN 1 ELSE 0 END), 1) AS pct_ai_posts
FROM posts
GROUP BY month
ORDER BY month;

-- Q4
SELECT
    ROUND(AVG(applications), 1) AS avg_applications,
    MEDIAN(applications)        AS median_applications,
    ROUND(AVG(interviews), 1)   AS avg_interviews,
    MEDIAN(interviews)          AS median_interviews,
    ROUND(AVG(offers), 1)       AS avg_offers,
    MEDIAN(offers)              AS median_offers
FROM posts;


-- Q5 -Interview rate: out of every 100 applications, how many led to an interview?
 
SELECT
    COUNT(*)                                             AS posts_used,
    ROUND(100.0 * SUM(interviews) / SUM(applications), 2) AS interviews_per_100_apps
FROM posts
WHERE applications IS NOT NULL
  AND interviews   IS NOT NULL;


-- Q6- The 10 posts with the most applications.
SELECT
    title,
    applications,
    interviews,
    offers
FROM posts
WHERE applications IS NOT NULL
ORDER BY applications DESC
LIMIT 10;
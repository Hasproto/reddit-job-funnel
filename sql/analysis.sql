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

-- analysis.sql

-- Tables: posts -one row per post- and monthly_summary -one row per month-
 


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

-- Q4  For posts that report numbers, what are the typical values?
SELECT
    ROUND(AVG(applications), 1) AS avg_applications,
    MEDIAN(applications) AS median_applications,
    ROUND(AVG(interviews), 1)   AS avg_interviews,
    MEDIAN(interviews) AS median_interviews,
    ROUND(AVG(offers), 1) AS avg_offers,
    MEDIAN(offers)   AS median_offers
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

-- Q7-  Did people who got an offer send fewer applications than people who did not?
SELECT
    CASE WHEN offers > 0 
    THEN 'got offer' 
    ELSE 'no offer' 
    END AS outcome,

    COUNT(*) AS posts,
    MEDIAN(applications) AS median_applications
FROM posts
WHERE applications IS NOT NULL
  AND offers  IS NOT NULL
GROUP BY outcome;


-- Q8- Do posts that mention AI get more comments?
SELECT
    mentions_ai,
    COUNT(*) AS posts,
    ROUND(AVG(num_comments), 1) AS avg_comments
FROM posts
GROUP BY mentions_ai;


-- Q9-  Data quality check: impossible numbers  
 
SELECT
    title,
    applications,
    interviews
FROM posts
WHERE interviews > applications;
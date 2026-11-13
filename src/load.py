# load.py
# Step 3 of the pipeline: put the clean posts into a database

import duckdb

CSV_FILE = "data/clean/posts_clean.csv"
DB_FILE = "data/jobs.duckdb"

# Open the database file (it is created if it does not exist)
con = duckdb.connect(DB_FILE)

# Copy all clean posts from the CSV file into a table called posts
con.execute(f"CREATE OR REPLACE TABLE posts AS SELECT * FROM read_csv_auto('{CSV_FILE}')")

# Data quality checks: count total posts and duplicate posts, and posts with no date
total = con.sql("SELECT COUNT(*) FROM posts").fetchall()[0][0]
duplicates = con.sql("SELECT COUNT(*) - COUNT(DISTINCT id) FROM posts").fetchall()[0][0]
missing_dates = con.sql("SELECT COUNT(*) FROM posts WHERE created_at IS NULL").fetchall()[0][0]

# Stop the pipeline if any check fails
if total == 0:
    raise ValueError("No posts were loaded. Check the extract and transform steps.")
if duplicates > 0:
    raise ValueError(f" Found {duplicates} duplicate post IDs.")
if missing_dates > 0:
    raise ValueError(f" Found {missing_dates} posts with no date.")
print(f"Quality checks passed: {total} posts, no duplicates, no missing dates")

# Build a small table with one row per month for the dashboard
con.execute("""
    CREATE OR REPLACE TABLE monthly_summary AS
    SELECT
        strftime(created_at, '%Y-%m') AS month,
        COUNT(*)                      AS total_posts,
        COUNT_IF(mentions_ai)         AS ai_posts,
        COUNT(applications)           AS posts_with_numbers,
        MEDIAN(applications)          AS median_applications,
        MEDIAN(interviews)            AS median_interviews,
        MEDIAN(offers)                AS median_offers
    FROM posts
    GROUP BY month
    ORDER BY month
""")

# Show the monthly table in the terminal
con.sql("SELECT * FROM monthly_summary").show()

# Close the database when done
con.close()
print(f"Saved database to {DB_FILE}")
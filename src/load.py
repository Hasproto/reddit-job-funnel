# load.py 
# Loads the clean CSV into DuckDB and builds a monthly summary table.
# Run from the project folder: python src/load.py

import duckdb

INPUT_FILE = "data/clean/posts_clean.csv"

 # created if it doesn't exist
DB_FILE = "data/jobs.duckdb"   


def main():
    con = duckdb.connect(DB_FILE)

    # CREATE OR REPLACE: safe to rerun; rebuilds the table each time.
    # read_csv_auto: DuckDB guesses column types from the CSV.
    con.execute(f"""
        CREATE OR REPLACE TABLE posts AS
        SELECT * FROM read_csv_auto('{INPUT_FILE}')
    """)

    count = con.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    print(f"Loaded {count} posts into the 'posts' table")

    # COUNT(applications) skips empty (NULL) values, unlike COUNT(*).
    # MEDIAN instead of AVG: a few huge numbers ( 2,000 applications)
    # would distort the average.
    con.execute("""
        CREATE OR REPLACE TABLE monthly_summary AS
        SELECT
            strftime(created_at, '%Y-%m')               AS month,
            COUNT(*)                                     AS total_posts,
            SUM(CASE WHEN mentions_ai THEN 1 ELSE 0 END) AS ai_posts,
            COUNT(applications)                          AS posts_with_numbers,
            MEDIAN(applications)                         AS median_applications,
            MEDIAN(interviews)                           AS median_interviews,
            MEDIAN(offers)                               AS median_offers
        FROM posts
        GROUP BY month
        ORDER BY month
    """)

    print("\nMonthly summary:")
    con.sql("SELECT * FROM monthly_summary").show()

    con.close()
    print(f"Saved database to {DB_FILE}")


if __name__ == "__main__":
    main()
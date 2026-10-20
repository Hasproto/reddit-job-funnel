# dashboard.py
# Show the results from the DuckDB database as a web page.

import duckdb
import streamlit as st

DB_FILE = "data/jobs.duckdb"

# ---------- Page title ----------
st.title("Reddit Job-Search Funnel")
st.write(
    "Job-search numbers that r/cscareerquestions users report about themselves "
    "(applications, interviews, offers). These are self-reported, not official statistics."
)

# ---------- Get data from the database ----------
con = duckdb.connect(DB_FILE, read_only=True)

# Overall totals (one row)
totals = con.sql("""
    SELECT
        COUNT(*)  AS total_posts,
        SUM(CASE WHEN mentions_ai THEN 1 ELSE 0 END) AS ai_posts,
        COUNT(applications) AS posts_with_numbers
    FROM posts
""").df()

# The monthly summary table that load.py built
summary = con.sql("SELECT * FROM monthly_summary").df()

# Posts that report a number of applications, biggest first
funnel_posts = con.sql("""
    SELECT created_at, title, applications, interviews, offers
    FROM posts
    WHERE applications IS NOT NULL
    ORDER BY applications DESC
""").df()

con.close()

# ---------- Big numbers at the top ----------
# st.columns(3) splits the page into 3 side-byside boxes
col1, col2, col3 = st.columns(3)
col1.metric("Total posts", int(totals["total_posts"][0]))
col2.metric("Posts mentioning AI", int(totals["ai_posts"][0]))
col3.metric("Posts with job-search numbers", int(totals["posts_with_numbers"][0]))

# ---------- Monthly table ----------
st.subheader("Monthly summary")
st.dataframe(summary)

# ---------- Chart: share of posts mentioning AI ----------

# Share (percent) is fairer than a raw count, because some months have more posts.
# (my old project used raw counts, which made recent months look bigger.)

st.subheader("Share of posts mentioning AI, by month")
summary["ai_share"] = summary["ai_posts"] / summary["total_posts"]
st.line_chart(summary, x="month", y="ai_share")

# ---------- Chart: median applications per month ----------

st.subheader("Median applications reported, by month")
st.bar_chart(summary, x="month", y="median_applications")

# ---------- Table of the actual posts ----------

st.subheader("Posts that report job-search numbers")
st.dataframe(funnel_posts)
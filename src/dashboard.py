# dashboard.py
# Shows the pipeline results as a web page.
# how to run Run: streamlit run src/dashboard.py

import duckdb
import os
import pandas as pd
import streamlit as st

# stop with a message if the pipeline has not been run yet
if not os.path.exists("data/jobs.duckdb"):
    st.error("No database found. Run: python run_pipeline.py")
    st.stop()

# Read the data from the database  
con = duckdb.connect("data/jobs.duckdb", read_only=True)
summary = con.sql("SELECT * FROM monthly_summary ORDER BY month").df()
posts = con.sql("""
    SELECT created_at, title, applications, interviews, offers
    FROM posts
    WHERE applications IS NOT NULL
    ORDER BY applications DESC
""").df()
con.close()

# Title
st.title("Reddit Job-Search Funnel")
st.write("Self-reported job-search numbers from r/cscareerquestions.")

# Big numbers at the top, in 3 side-by-side boxes
total = int(summary["total_posts"].sum())
ai_percent = 100 * summary["ai_posts"].sum() / total

col1, col2, col3 = st.columns(3)
col1.metric("Total posts", f"{total:,}")                
col2.metric("Posts mentioning AI", f"{ai_percent:.1f}%")   
col3.metric("Posts with numbers", len(posts))

# Line chart: percent of posts about AI each month
 
st.subheader("Percent of posts mentioning AI, by month")
summary["ai_percent"] = 100 * summary["ai_posts"] / summary["total_posts"]
st.line_chart(summary, x="month", y="ai_percent")

# Bar chart: the funnel  
st.subheader("Typical funnel (median per post)")
funnel = pd.DataFrame({
    "stage": ["1. Applications", "2. Interviews", "3. Offers"],
    "median": [posts["applications"].median(),
               posts["interviews"].median(),
               posts["offers"].median()],
})
st.bar_chart(funnel, x="stage", y="median")

# Tables ( 
st.subheader("Monthly summary")
st.dataframe(summary, hide_index=True)

st.subheader("Posts with job-search numbers")
st.dataframe(posts, hide_index=True)

# Note for viewers
st.caption("Numbers are self-reported and may be biased toward very good or very bad results.")
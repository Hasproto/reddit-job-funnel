# Data Dictionary

This file explains every dataset and column in the pipeline: what it means, where it comes from, and known problems.

## Pipeline overview

| Stage | File / Table | Created by | Description |
|---|---|---|---|
| Raw | `data/raw/posts.json` | `src/extract.py` | Posts exactly as downloaded from the Arctic Shift API |
| Clean | `data/clean/posts_clean.csv` | `src/transform.py` | Cleaned posts with extracted job-search numbers |
| Database | `posts` table in `data/jobs.duckdb` | `src/load.py` | Same as the clean CSV, stored in DuckDB |
| Summary | `monthly_summary` table in `data/jobs.duckdb` | `src/load.py` | One row per month, used by the dashboard |
**Source:** public posts from r/cscareerquestions, collected through the [Arctic Shift](https://github.com/ArthurHeitmann/arctic_shift) archive API.
**Grain** (what one row means): `posts` = one Reddit post. `monthly_summary` = one calendar month.

---

## 1. Raw data: `data/raw/posts.json`

| Column | Type | Description |
|---|---|---|
| `id` | text | Reddit's unique ID for the post |
| `title` | text | Post title |
| `selftext` | text | Post body. `[removed]` or `[deleted]` if taken down |
| `author` | text | Username (dropped during cleaning for privacy) |
| `created_utc` | integer | Post time in seconds since Jan 1, 1970 (UTC) |
| `score` | integer | Upvotes minus downvotes at time of download |
| `num_comments` | integer | Number of comments at time of download |
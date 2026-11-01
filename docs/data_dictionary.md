# Data Dictionary

This file explains every dataset and column in the pipeline: what it means, where it comes from, and known problems.

## Pipeline overview

| Stage | File / Table | Created by | Description |
|---|---|---|---|
| Raw | `data/raw/posts.json` | `src/extract.py` | Posts exactly as downloaded from the Arctic Shift API |
| Clean | `data/clean/posts_clean.csv` | `src/transform.py` | Cleaned posts with extracted job-search numbers |
| Database | `posts` table in `data/jobs.duckdb` | `src/load.py` | Same as the clean CSV, stored in DuckDB |
| Summary | `monthly_summary` table in `data/jobs.duckdb` | `src/load.py` | One row per month, used by the dashboard |
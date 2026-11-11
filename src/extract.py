# extract.py
# EXTRACT
# Download Reddit posts from the Arctic Shift archive and save them as a JSON file.
     

import json    
import os
import time   
import requests   

# Settings  

# The Arctic Shift web address for searching posts
URL = "https://arctic-shift.photon-reddit.com/api/posts/search"

SUBREDDIT = "cscareerquestions"

# Date range. 
START_DATE = "2024-01-01"
END_DATE = "2024-02-01"

# Where to save the downloaded posts  
OUTPUT_FILE = "data/raw/posts.json"

# Only ask for the columns we need  
FIELDS = "id,title,selftext,author,created_utc,score,num_comments"


# ---------- Functions -----------------------------------------------

def get_one_page(after):
    """Ask the API for up to 100 posts created after the time 'after'.
    Returns a list of posts, where each post is a dictionary."""

     
    params = {
        "subreddit": SUBREDDIT,
        "after": after,         # only posts newer than this time
        "before": END_DATE,     # only posts older than this date
        "sort": "asc",          # oldest first
        "limit": 100,           # the maximum the API allows per request
        "fields": FIELDS,
    }

    # Try up to 3 times. because the internet or the server can fail for a moment
    for attempt in range(3):
        try:
            response = requests.get(URL, params=params, timeout=60)
            response.raise_for_status()
            return response.json()["data"]
        except requests.RequestException as error:
            print(f"Request failed: {error}. Trying again in 10 seconds...")
            time.sleep(10)

    # Failed 3 times in a row. So ,stop with a clear message
    raise RuntimeError("The API failed 3 times in a row. Stopping.")  

     

     

def main():
    """Download all pages and save every post into one file."""
    all_posts = []      # every post we collect
    seen_ids = set()    # post IDs we already have (to skip duplicates)
    after = START_DATE  # start from the beginning of the date range

    while True:
        page = get_one_page(after)

        # Keep only posts we haven't seen before
        new_posts = [post for post in page if post["id"] not in seen_ids]

        # Nothing new means we've reached the end
        if len(new_posts) == 0:
            break

        for post in new_posts:
            all_posts.append(post)
            seen_ids.add(post["id"])

        print(f"Downloaded {len(all_posts)} posts so far...")

        # Fewer than 100 posts means this was the last page
        if len(page) < 100:
            break

        # Next page starts at the time of the newest post we got.
        # created_utc = post time in seconds since Jan 1, 1970 (the API accepts this format)
        # Go back 1 second so posts made in the same second aren't skipped (seen_ids removes repeats)
        after = page[-1]["created_utc"] -1

        # Wait 1 second so we don't overload this free service
        time.sleep(1)

    #Create the folder if it does not exist 
    os.makedirs("data/raw", exist_ok=True)    

    # Save all posts to a JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_posts, f)

    print(f"Done! Saved {len(all_posts)} posts to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
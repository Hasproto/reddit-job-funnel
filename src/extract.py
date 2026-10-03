# extract.py
# EXTRACT
# Download Reddit posts from the Arctic Shift archive and save them as a JSON file.
     

import json    
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

    response = requests.get(URL, params=params, timeout=60)

    # If the server returned an error ,stop  
    response.raise_for_status()

    # The API sends back
    return response.json()["data"]

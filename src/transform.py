# transform.py
 
import re             
import pandas as pd  

INPUT_FILE = "data/raw/posts.json"
OUTPUT_FILE = "data/clean/posts_clean.csv"


APPLICATION_PATTERNS = [
    r"(\d[\d,]*)\+?\s*(?:job\s+)?(?:applications|apps)\b",       # "350 applications", "500+ apps"
    r"applied to (?:over |about |around )?(\d[\d,]*)",           # "applied to over 200"
]
INTERVIEW_PATTERNS = [
    r"(\d[\d,]*)\s+interviews?\b",                               # "12 interviews", "1 interview"
]
OFFER_PATTERNS = [
    r"(\d[\d,]*)\s+offers?\b",                                   # "2 offers", "1 offer"
]

AI_PATTERN = (
    r"\b(?:ai|a\.i|artificial intelligence|gen ?ai|generative ai"
    r"|chat ?gpt|gpts?|gpt-?\d\w*|openai|anthropic"
    r"|llms?|large language models?|copilot|claude|gemini)\b"
)
def clean_posts(df):
    """Remove bad rows and build one 'text' column from title + body."""
    df = df.drop_duplicates(subset="id")                      
    df = df[~df["selftext"].isin(["[removed]", "[deleted]"])]  # ~ means NOT
    df = df[df["author"] != "AutoModerator"]                    
    df = df.copy()  # make a fresh copy so pandas doesn't warn when we add columns below

    df["selftext"] = df["selftext"].fillna("")                 # instead of #
    df["text"] = df["title"] + " " + df["selftext"]            # one column to search in

    # created_utc is seconds epcoch or sth
    df["created_at"] = pd.to_datetime(df["created_utc"], unit="s")

    # no usernames for the analysis, so drop them for privacy
    df = df.drop(columns=["author", "selftext", "created_utc"])


    
    return df
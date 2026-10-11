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

def find_number(text, patterns):
    """Try each pattern; return the first number found, or None if nothing matches."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)   # IGNORECASE: "Offers" = "offers"
        if match:
            number_text = match.group(1)                   # group(1) = the part inside ( )
            return int(number_text.replace(",", ""))       
    return None


def add_number_columns(df):
    """Add applications / interviews / offers columns using the patterns above."""
    # apply runs a function on every row of the column.
    df["applications"] = df["text"].apply(lambda t: find_number(t, APPLICATION_PATTERNS))
    df["interviews"] = df["text"].apply(lambda t: find_number(t, INTERVIEW_PATTERNS))
    df["offers"] = df["text"].apply(lambda t: find_number(t, OFFER_PATTERNS))

    for col in ["applications", "interviews", "offers"]:
        df[col] = df[col].astype("Int64")
    return df

# transform.py
# Clean the posts and find job-search numbers in the text.


import os
import re
import pandas as pd

INPUT_FILE = "data/raw/posts.json"
OUTPUT_FILE = "data/clean/posts_clean.csv"

# Patterns to find numbers in text.
# (\d[\d,]*) = a number like 350 or 1,200. The ( ) keeps that number.
APPLICATION_PATTERNS = [
    r"(\d[\d,]*)\+?\s*(?:job\s+)?(?:applications|apps)\b",  # "350 applications", "500+ apps"
    r"applied to (?:over |about |around )?(\d[\d,]*)",      # "applied to over 200"
]
INTERVIEW_PATTERNS = [r"(\d[\d,]*)\s+interviews?\b"]       # "12 interviews", "1 interview"
OFFER_PATTERNS = [r"(\d[\d,]*)\s+offers?\b"]               # "2 offers", "1 offer"

# Find AI words only as whole words (\b = edge of a word),
# so "said" and "email" don't count (the old project's bug).
AI_PATTERN = r"\b(?:ai|artificial intelligence|chatgpt|llms?|copilot)\b"


def find_number(text, patterns):
    """Return the first number the patterns find, or None if nothing matches."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1).replace(",", ""))  # "1,200" -> 1200
    return None


def main():
    df = pd.read_json(INPUT_FILE)
    print(f"Raw posts: {len(df)}")

    # 1. Remove duplicates, deleted posts, and the subreddit's bot
    df = df.drop_duplicates(subset="id")
    df = df[~df["selftext"].isin(["[removed]", "[deleted]"])]  # ~ means NOT
    df = df[df["author"] != "AutoModerator"].copy()            # copy() avoids a pandas warning
    print(f"Clean posts: {len(df)}")

    # 2. Make one text column and a real date column
    df["text"] = df["title"] + " " + df["selftext"].fillna("")
    df["created_at"] = pd.to_datetime(df["created_utc"], unit="s")  # seconds -> date

    # 3. Go through each post and find the numbers and AI mentions
    applications = []
    interviews = []
    offers = []
    mentions_ai = []
    cleared = 0

    for text in df["text"]:
        apps = find_number(text, APPLICATION_PATTERNS)
        ints = find_number(text, INTERVIEW_PATTERNS)
        offs = find_number(text, OFFER_PATTERNS)

        # More interviews than applications = extraction mistake, so clear the numbers
        if apps is not None and ints is not None and ints > apps:
            apps, ints, offs = None, None, None
            cleared += 1

        applications.append(apps)
        interviews.append(ints)
        offers.append(offs)
        mentions_ai.append(re.search(AI_PATTERN, text, re.IGNORECASE) is not None)

    df["applications"] = applications
    df["interviews"] = interviews
    df["offers"] = offers
    df["mentions_ai"] = mentions_ai

    # "Int64" = whole numbers that can be empty (otherwise 350 shows as 350.0)
    for col in ["applications", "interviews", "offers"]:
        df[col] = df[col].astype("Int64")

    # 4. Drop columns we don't need anymore (author dropped for privacy)
    df = df.drop(columns=["author", "selftext", "created_utc"])

    # 5. Print a short summary and save
    print(f"Cleared {cleared} posts with impossible numbers")
    print(f"Posts with application numbers: {df['applications'].notna().sum()}")
    print(f"Posts mentioning AI: {sum(mentions_ai)}")

    os.makedirs("data/clean", exist_ok=True)  # create the folder if it's missing
    df.to_csv(OUTPUT_FILE, index=False)       # index=False: don't save row numbers
    print(f"Saved to {OUTPUT_FILE}")


# Run main() only when this file is run directly
if __name__ == "__main__":
    main()
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

 
AI_PATTERN = r"\b(?:ai|artificial intelligence|chatgpt|llms?|copilot)\b"

# add or modify the AI_PATTERN later.
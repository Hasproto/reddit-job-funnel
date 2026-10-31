# test_transform.py
# Small checks that the number_finding code in transform.py works.
#
# To run from the project folder: python -m pytest

import re

from src.transform import (
    find_number,
    APPLICATION_PATTERNS,
    INTERVIEW_PATTERNS,
    OFFER_PATTERNS,
    AI_PATTERN,
)


# find_number()  

def test_finds_applications():
    assert find_number("I sent 350 applications", APPLICATION_PATTERNS) == 350


def test_handles_commas():
    
    assert find_number("1,200 apps and nothing", APPLICATION_PATTERNS) == 1200


def test_applied_to_wording():
    assert find_number("I applied to over 200 jobs", APPLICATION_PATTERNS) == 200


def test_ignores_upper_case():
    assert find_number("350 APPLICATIONS", APPLICATION_PATTERNS) == 350

def test_finds_single_interview():
    # "interview" (no s) should work too
    assert find_number("only 1 interview so far", INTERVIEW_PATTERNS) == 1


def test_finds_offers():
    assert find_number("finally got 2 offers", OFFER_PATTERNS) == 2


def test_returns_none_when_no_number():
    assert find_number("any advice for my resume?", APPLICATION_PATTERNS) is None


#                      AI_PATTERN (the fix for the old bug) 

def mentions_ai(text):
    """Helper: True if the AI pattern finds a match in the text."""
    return re.search(AI_PATTERN, text, re.IGNORECASE) is not None


def test_ai_word_is_found():
    assert mentions_ai("Will AI replace junior devs?")


def test_chatgpt_is_found():
    assert mentions_ai("ChatGPT helped with my resume")


def test_old_bug_words_are_not_ai():
    # The old project counted these as AI because they contain the letters "ai"
    assert not mentions_ai("I said I would email again")
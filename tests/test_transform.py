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
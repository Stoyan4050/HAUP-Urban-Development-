"""
calculate_greenery_rounded.py
"""

from math import ceil


def calculate_greenery_rounded(contains_greenery, greenery_percentage):
    """
    def calculate_greenery_rounded(contains_greenery, greenery_percentage)
    """

    if not contains_greenery:
        return 0

    if contains_greenery and greenery_percentage == 0:
        return 25

    return int(25 * ceil(100 * greenery_percentage / 25))

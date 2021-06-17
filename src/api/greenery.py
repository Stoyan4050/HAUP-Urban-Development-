"""
greenery.py
"""
from math import ceil
from classification.classifier import find_color_image


def calculate_greenery_rounded(contains_greenery, greenery_percentage):
    """
    def calculate_greenery_rounded(contains_greenery, greenery_percentage)
    """

    if not contains_greenery:
        return 0

    if contains_greenery and greenery_percentage == 0:
        return 25

    return int(25 * ceil(100 * greenery_percentage / 25))


def calculate_percentage_greenery(x_esri, y_esri, year, contains_greenery):
    """
    def calculate_percentage_greenery(x_esri, y_esri, year, contains_greenery)
    """

    first_colored_map = 1914

    if contains_greenery:
        return find_color_image(x_esri, y_esri, max(year, first_colored_map))

    return 0

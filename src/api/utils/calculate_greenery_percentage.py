"""
calculate_greenery_percentage.py
"""

from classification.classifier import find_color_image


def calculate_greenery_percentage(x_esri, y_esri, year, contains_greenery):
    """
    def calculate_greenery_percentage(x_esri, y_esri, year, contains_greenery)
    """

    first_colored_map = 1914

    if contains_greenery:
        return find_color_image(x_esri, y_esri, max(year, first_colored_map))

    return 0

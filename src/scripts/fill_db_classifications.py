"""
fill_db_classifications.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from api.utils import euclidean_distance_random_tiles


def run():
    """
    def run()
    """

    euclidean_distance_random_tiles()

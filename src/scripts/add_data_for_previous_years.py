"""
fill_db_classifications.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from api.utils import add_labels_for_previous_years


def run():
    """
    def run()
    """

    add_labels_for_previous_years()

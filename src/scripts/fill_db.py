"""
fill_db.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from api.utils import extract_convert_to_esri


def run():
    """
    def run()
    """

    extract_convert_to_esri()

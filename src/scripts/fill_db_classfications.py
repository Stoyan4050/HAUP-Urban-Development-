"""
fill_db_classfications.py
"""

import os
import sys
from api.utils import extract_convert_to_esri

sys.path.insert(0, os.path.abspath('..'))


def run():
    """
    def run()
    """

    extract_convert_to_esri()

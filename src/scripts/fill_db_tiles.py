"""
fill_db_tiles.py
"""

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from api.utils import create_tiles


def run():
    """
    def run()
    """

    create_tiles()

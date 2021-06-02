"""
fill_db_tiles.py
"""

import os
import sys
from api.utils import create_tiles

sys.path.insert(0, os.path.abspath('..'))


def run():
    """
    def run()
    """

    create_tiles()

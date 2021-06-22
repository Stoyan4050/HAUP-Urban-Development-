"""
classify_tile_view.py
"""

import json
from django.views import View
from classification.classifier_cnn import classify_cnn


class ClassifyTileView(View):
    """
    class ClassifyTileView(View)
    """

    @staticmethod
    def get(_, parameters):
        """
        @staticmethod
        def get(_, parameters)
        """

        year = json.loads(parameters).get("year")

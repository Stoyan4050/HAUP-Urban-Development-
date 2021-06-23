"""
classification_manager.py
"""

from django.db import models
from django.utils.translation import ugettext_lazy


class ClassificationManager(models.Manager):
    """
    class ClassificationManager(models.Manager)
    """

    def create_classification(self, tile, year, classified_by, contains_greenery, greenery_percentage):
        """
        def create_classification(self, tile, year, greenery_percentage, classified_by)
        """

        if not tile:
            raise ValueError(ugettext_lazy("A classification cannot be created without a tile."))

        classification = self.create(tile=tile, year=year, classified_by=classified_by,
                                     contains_greenery=contains_greenery, greenery_percentage=greenery_percentage)
        return classification

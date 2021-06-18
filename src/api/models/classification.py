"""
classification.py
"""

from django.db import models
from api.models.classification_manager import ClassificationManager


class Classification(models.Model):
    """
    class Classification(models.Model)
    """
    class Meta:
        """
        class Meta
        """
        unique_together = ["year", "tile"]
        ordering = ["year", "tile"]

    classification_id = models.AutoField(primary_key=True, null=False, unique=True)
    year = models.IntegerField(null=False)
    tile = models.ForeignKey("Tile", db_column="tile_id", on_delete=models.CASCADE, null=False)
    classified_by = models.IntegerField(null=False)
    contains_greenery = models.BooleanField(null=False)
    greenery_percentage = models.FloatField(null=False)
    REQUIRED_FIELDS = [tile, year, classified_by, contains_greenery, greenery_percentage]
    objects = ClassificationManager()

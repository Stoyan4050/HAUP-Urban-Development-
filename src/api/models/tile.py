"""
tile.py
"""

from django.db import models
from api.models.tile_manager import TileManager


class Tile(models.Model):
    """
    class Tile(models.Model)
    """
    class Meta:
        """
        class Meta
        """
        unique_together = ["x_coordinate", "y_coordinate"]
        ordering = ["x_coordinate", "y_coordinate"]

    tile_id = models.BigIntegerField(primary_key=True, null=False, unique=True)
    x_coordinate = models.IntegerField(null=False)
    y_coordinate = models.IntegerField(null=False)
    REQUIRED_FIELDS = [tile_id, x_coordinate, y_coordinate]
    objects = TileManager()

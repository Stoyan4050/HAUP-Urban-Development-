"""
models_old.py
"""

from django.db import models
from django.utils.translation import ugettext_lazy


class TileManager(models.Manager):
    """
    class TileManager(models.Manager)
    """

    def create_tile(self, tile_id, x_coordinate, y_coordinate):
        """
        def create_tile(self, x_coordinate, y_coordinate)
        """

        if not tile_id or not x_coordinate or not y_coordinate:
            raise ValueError(ugettext_lazy("You cannot save a tile without an id, x and y coordinates."))

        tile = self.create(tile_id=tile_id, x_coordinate=x_coordinate, y_coordinate=y_coordinate)
        return tile


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

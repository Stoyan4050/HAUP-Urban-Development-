"""
tile_manager.py
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

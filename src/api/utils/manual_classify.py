"""
manual_classify.py
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from api.models.user import User
from api.models.classification import Classification
from api.models.tile import Tile
from api.utils.transform_coordinates_to_tile import transform_coordinates_to_tile


def manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery):
    """
    def manual_classify(x_coordinate, y_coordinate, year, user, greenery_percentage, contains_greenery):
    """

    x_tile, y_tile = transform_coordinates_to_tile(x_coordinate, y_coordinate)
    tile_id = x_tile * 75879 + y_tile

    try:
        Classification.objects.create(tile=Tile(tile_id, x_tile, y_tile),
                                      year=year, greenery_percentage=greenery_percentage,
                                      contains_greenery=contains_greenery,
                                      classified_by=User.objects.get(email=user).id)

    except IntegrityError:
        Classification.objects.filter(year=year, tile=Tile(tile_id, x_tile, y_tile)) \
            .update(greenery_percentage=greenery_percentage, contains_greenery=contains_greenery,
                    classified_by=User.objects.get(email=user).id)

    except ObjectDoesNotExist:
        print("Unsuccessfully updated tiles.")

from .models import Tile, Classification

def add_user_label(start_x, start_y, length_x, length_y, year, label, user_id):

    for x in range(start_x, start_x + length_x - 1):
        for y in range(start_y, start_y + length_y - 1):

            try:
                Classification.objects.create(tile_id=Tile.objects.get(x_coordinate=x, y_coordinate=y), year=year,
                                              label=label, classified_by=user_id)
            except Tile.DoesNotExist:
                print(x, y)
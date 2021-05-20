class TileToCoordinatesTransformer():
    _x_offset = 406.40102300613496932515337423313
    _y_offset = 406.40607802340702210663198959688

    def transform(self, x_tile, y_tile):
        xmin = x_tile - 75120
        xmin *= self._x_offset
        xmin = xmin + 13328.546
        
        ymax = y_tile - 75032
        ymax *= self._y_offset
        ymax = 619342.658 - ymax

        xmax = xmin + self._x_offset
        ymin = ymax - self._y_offset

        x_coordinate = (xmin + xmax) / 2
        y_coordinate = (ymin + ymax) / 2

        return {
            "xmin": xmin,
            "ymin": ymin,
            "xmax": xmax,
            "ymax": ymax,
            "x_coordinate": x_coordinate,
            "y_coordinate": y_coordinate,
        }

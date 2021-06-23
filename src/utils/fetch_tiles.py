"""
fetch_tiles.py
"""

import urllib.request


def fetch_tiles(year, range_x, range_y, folder):
    """
    def fetch_tiles(year, range_x, range_y, folder)
    """

    for x_coord in range_x:
        for y_coord in range_y:

            res = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" +\
                  str(year) + "/MapServer/tile/11/" + str(x_coord) + "/" + str(y_coord)

            urllib.request.urlretrieve(res, "../" + folder + "/" + str(y_coord) + "_" + str(x_coord) + ".png")


if __name__ == "__main__":
    fetch_tiles(2020, range(75748, 75879), range(75087, 75825), "")

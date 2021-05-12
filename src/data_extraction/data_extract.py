from math import floor

from pyproj.transformer import TransformerGroup
import pandas


def extract_convert_to_esri():
    tg = TransformerGroup("epsg:4326", "epsg:28992")
    col_list = ['item', 'geo']

    # Change here the name of the input file
    df = pandas.read_csv("parks.csv", names=col_list)

    points = df.geo.tolist()

    points.pop(0)

    # Change here the name of the output file
    f = open("parks_tiles.txt", "a")

    for location in points:
        before_flip = location.split("(")[1][:-1]
        x = before_flip.split(" ")[1]
        y = before_flip.split(" ")[0]

        x_esri = tg.transformers[0].transform(x, y)[0]
        y_esri = tg.transformers[0].transform(x, y)[1]

        x_esri -= 13328.546
        x_esri /= 406.40102300613496932515337423313

        y_esri = 619342.658 - y_esri
        y_esri /= 406.40607802340702210663198959688

        x_esri = floor(x_esri) + 75120
        y_esri = floor(y_esri) + 75032

        f.write("https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_2020/MapServer/tile/11/" + str(y_esri) + "/" + str(x_esri) + "\n")

    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    extract_convert_to_esri()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""
add_labels_to_csv.py
"""

from csv import writer
import pandas


# This script reads csv files extracted from wikidata and places all relevant information from them into data.csv
# It also adds the data label, which can be entered in by the user
def add_label():
    """
    def add_label()
    """

    print("Please enter the file wish to read")
    file_name = input()
    data_frame = pandas.read_csv("./data/Wikidata/" + file_name)

    print("Please enter in desired label name")
    label_name = input()
    points = data_frame.geo.tolist()

    years = ["Unknown" for _ in range(len(data_frame))]
    if 'inception' in data_frame.columns:
        years = data_frame.inception.tolist()

    with open("./data/Wikidata/data.csv", "a") as f_object:
        writer_object = writer(f_object)

        for ind in enumerate(points):
            args = [points[ind], years[ind], label_name]
            writer_object.writerow(args)

        f_object.close()


if __name__ == "__main__":
    add_label()

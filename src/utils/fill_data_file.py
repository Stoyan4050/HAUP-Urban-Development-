"""
fill_data_file.py
"""

from csv import writer
import pandas


# This script reads csv files extracted from wikidata and places all relevant information from them into data.csv
# It also adds the data label, which can be entered in by the user
def fill_file():
    """
    def fill_file()
    """

    file_names = []
    while (True):
        print("Please enter the file wish to read or leave empty, if there are no more files to read")
        file_name = input()

        if file_name == "":
            break

        file_names.append(file_name)

    if file_names:
        with open("../data/Wikidata/data.csv", "a", newline="") as f_object:
            writer_object = writer(f_object)
            for file_name in file_names:
                data_frame = pandas.read_csv("../data/Wikidata/" + file_name)
                points = data_frame.geo.tolist()
                years = ["Unknown" for _ in range(len(data_frame))]

                if 'inception' in data_frame.columns:
                    years = data_frame.inception.tolist()

                for index in range(len(points)):
                    args = [points[index], years[index]]
                    writer_object.writerow(args)

            f_object.close()


if __name__ == "__main__":
    fill_file()

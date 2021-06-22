"""
create_empty_data_file.py
"""

import csv
from pathlib import Path


def create_empty_data_file():
    """
    Creates a new file named data.csv and initializes all the proper column names.
    """

    my_file = Path("../data/Wikidata/data.csv")
    if my_file.is_file():
        answer = None
        while answer is None:
            print("There is already a data file in the data directory. "
                  "Proceeding further will delete all records stored within it."
                  "Would you still like to continue (Y/N):")
            inp = input()
            if inp.lower() == "y":
                answer = True
            elif inp.lower() == "n":
                answer = False
        if not answer:
            print("Aborted")
            return

    with open("../data/Wikidata/data.csv", "w", newline="") as data:
        file_writer = csv.writer(data, delimiter=",")
        file_writer.writerow(["geo", "inception", "contains_greenery"])


if __name__ == "__main__":
    create_empty_data_file()

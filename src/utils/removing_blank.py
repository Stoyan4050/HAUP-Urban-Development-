"""
removing_blank.py
"""

from csv import writer
import os
import cv2
import numpy as np


def remove_blank():
    """
    This function takes all images from a set directory and writes all images, which are not blank (i.e. empty)
    into the folder the script is in. This way, we can filter out all placeholder tiles in the maps provided,
    which turn out to be over half the tiles.
    There is the issue of the saved images being very large in size, but since this script is only used for testing,
    research and development, this should not be a problem.
    """

    basepath = '../you_need_to_enter_this_in_yourself'
    entries = os.listdir(basepath)
    size = len(entries)
    curr = 0

    for index, entry in enumerate(entries):
        if index * 100 / size > curr:
            curr += 1
            print(curr, "%")

        if ".png" in entry:
            image = cv2.imread(basepath + "/" + entry, 1)
            avg = np.average(image)

            if avg > 0.01:
                cv2.imwrite(entry, image)


def export_nonblank_to_csv():
    """
    This function takes all images from a directory and outputs the filenames of all non-blank tiles into tilenames.csv.
    The point of this function is to have a textual representation of all tiles containing information,
    in order to only add them in the database.
    """

    basepath = '../you_need_to_enter_this_in_yourself'

    with open("./tilenames.csv", 'a') as f_object:
        writer_object = writer(f_object)
        curr = 0

        for index, i in enumerate(range(74956, 75879)):
            if index * 100 / (75879 - 74956) > curr:
                curr += 1
                print(curr, "%")
            for j in range(75087, 75825):
                entry = str(j) + "_" + str(i) + ".png"
                image = cv2.imread(basepath + "/" + entry, 1)
                avg = np.average(image)
                if avg > 0.000001:
                    result = [entry]
                    writer_object.writerow(result)

    f_object.close()


if __name__ == "__main__":
    # remove_blank()
    # export_nonblank_to_csv()

    print("Please uncomment one of the two commented lines of code to use the desired function.")

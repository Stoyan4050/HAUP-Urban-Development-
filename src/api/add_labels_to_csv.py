import pandas
from csv import writer

# This script reads csv files extracted from wikidata and places all relevant information from them into data.csv
# It also adds the data label, which can be entered in by the user
def add_label():

    file_name = input()
    df = pandas.read_csv("./data_extraction/" +file_name)
    label_name = input()
    points = df.geo.tolist()
    points.pop(0)

    flag = False
    years = []
    if 'inception' in df.columns:
        flag = True
        years = df.inception.tolist()
        years.pop(0)

    with open ("./data_extraction/data.csv", 'a') as f_object:
        writer_object = writer(f_object)
        for ind in range(len(points)):
            if(flag == True):
                List =[points[ind], years[ind], label_name]
            else:
                List = [points[ind], "Unknown", label_name]
            writer_object.writerow(List)

        f_object.close()


if __name__ == "__main__":
    add_label()

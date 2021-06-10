"""
classification_main.py
"""

from src.api import classifier
from src.api import classifier_new

if __name__ == "__main__":
    # main(1900 ,range(75400,75879),range(75400,75825),"1900")
    # img_path = "2020/75400_75437.png"

    #classifier.classify()
    classifier_new.classify_cnn()

"""
train_cnn.py
"""

from api.classifier import train_cnn


def run():
    """
        run classifier train_cnn
    """

    train_cnn(download_data=False)

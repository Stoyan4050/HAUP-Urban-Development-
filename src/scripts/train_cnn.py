from api.classifier import train_cnn


def run(*args):
    train_cnn(download_data=False)
from api.classifier import classify


def run(*args):
    classify(download_data=False)
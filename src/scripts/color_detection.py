from api.classifier import color_detection


def run():
    """
        run classifier train_cnn
    """

    color_detection(download_data=False)

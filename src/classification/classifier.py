"""
classifier.py
"""

from urllib.error import HTTPError
import urllib.request
import os
import cv2
import numpy as np
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow.keras import Sequential, layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
from api.models.classification import Classification

ALL_LABELS = ['beach', 'church', 'city square', 'garden', 'greenery', 'museum', 'not a public space',
              'park', 'recreational area']


def get_image_from_url(year, x_coord, y_coord):
    """
    Get historic map images from website.
    """

    url = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
        year) + "/MapServer/tile/11/" + str(x_coord) + "/" + str(y_coord)

    try:
        res = urllib.request.urlretrieve(url)
        img = cv2.imread(res[0], 1)
        return img
    except HTTPError:
        return None


def get_images_training(data, year):
    """
    Get images for training.
    """

    training_imgs = []
    counter = 0
    for classification in data:
        tile = classification.tile_id

        img = get_image_from_url(year, tile.y_coordinate, tile.x_coordinate)

        save_images(classification.label, img, counter, True)
        training_imgs.append((img, classification.label))

        print(counter)
        counter += 1

    return training_imgs


def get_images_test(year):
    """
    Get images for test.
    """

    Classification.objects.filter(classified_by=-1).delete()
    data = Classification.objects.filter(~Q(classified_by=-1))

    test_imgs = []
    counter = 0
    for classification in data:
        tile = classification.tile_id

        img = get_image_from_url(year, tile.y_coordinate, tile.x_coordinate)

        coord = (tile.y_coordinate, tile.x_coordinate)
        save_images(classification.label, img, counter, False)
        test_imgs.append((img, coord))
        print(counter)
        counter += 1

    return np.array(test_imgs)


def random_sample(arr):
    """
    Get random sample of the data.
    """

    arr = np.array(arr)
    res = arr[np.random.choice(len(arr), size=int(len(arr) / 2), replace=False)]
    return res


def get_labels_imgs(data):
    """
    Separate images and labels from the data.
    """

    labels = []
    imgs = []
    for img, label in data:
        labels.append(label)
        imgs.append(img)
    return np.array(labels), np.array(imgs)


def classify(year=2015, download_data=False):
    """
    Classify.
    """

    all_labels = ['beach', 'church', 'city square', 'garden', 'greenery', 'museum', 'not a public space', 'park',
                  'recreational area']
    # color_detection(75400, 75438)

    if download_data:
        create_dir(all_labels)
        get_images_training(Classification.objects.filter(year__lte=year), year)
        get_images_test(year)

    train_images, train_labels = read_images(all_labels, True)
    test_images, test_labels = read_images(all_labels, False)

    label_encoder = LabelEncoder()
    train_labels = label_encoder.fit_transform(train_labels)
    test_labels = label_encoder.transform(test_labels)

    train_images = np.array(train_images)
    test_images = np.array(test_images)
    # print("TEST", test_images)
    print("Training imgs loaded. Classification starts!")
    m_train, n_train, r_train, k_train = train_images.shape
    train_imgs_reshaped = train_images.reshape(m_train, n_train * r_train * k_train)

    m_test, n_test, r_test, k_test = test_images.shape
    test_imgs_reshaped = test_images.reshape(m_test, n_test * r_test * k_test)

    pipe = Pipeline([("pca", PCA(n_components=2)), ("svc", SVC(C=10, kernel="poly", random_state=42))])
    pipe.fit(train_imgs_reshaped, train_labels)
    prediction = pipe.predict(test_imgs_reshaped)

    print(accuracy_score(test_labels, prediction))
    print(classification_report(test_labels, prediction, target_names=label_encoder.classes_))


def create_dir(all_labels):
    """
    Creates directories for storing images. Takes in all labels for directory names.
    """

    path_train = "./data/train"
    path_test = "./data/test"
    # shutil.rmtree(path_train)
    # shutil.rmtree(path_test)
    os.makedirs(path_train)
    os.makedirs(path_test)

    for label in all_labels:
        new_path_train = path_train + "/" + label
        new_path_test = path_test + "/" + label
        os.makedirs(new_path_train)
        os.makedirs(new_path_test)


def save_images(label, img, counter, train=True):
    """
    Saves images in corresponding directory.
    Takes in label for directory, image to store, counter for unique file name.
    """

    if train:

        path = "./data/train"
        cv2.imwrite(path + "/" + label + "/train_img_" + str(counter) + ".jpg", img)
    else:
        path = "./data/test"
        cv2.imwrite(path + "/" + label + "/test_img_" + str(counter) + ".jpg", img)


def train_cnn(year=2015, download_data=False, train_network=True):
    """
    Train CNN.
    Takes in year of map, whether data needs to be downloaded and if network is trained.
    """

    if download_data:
        create_dir(ALL_LABELS)
        get_images_training(Classification.objects.filter(year__lte=year), year)
        get_images_test(year)

    train_images, train_labels = read_images(ALL_LABELS, True)

    # test_images = read_images(ALL_LABELS, False)
    # test_labels = read_images(ALL_LABELS, False)
    # print(len(train_images))
    # print("Training data extracted!")

    label_encoder = LabelEncoder()
    train_labels = label_encoder.fit_transform(train_labels)
    # test_labels = label_encoder.transform(test_labels)
    # print("Training images loaded. Classification starts!")

    train_images = train_images / 255.0

    train_images, train_labels = shuffle(train_images, train_labels, random_state=1)
    batch_size = 32
    checkpoint_path = "./model_checkpoint/cp-{epoch:04d}.ckpt"
    # checkpoint_dir = os.path.dirname(checkpoint_path)

    if train_network:
        model = Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Dropout(0.25))

        model.add(layers.Conv2D(64, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Dropout(0.25))

        model.add(layers.Conv2D(128, (3, 3), activation='relu', input_shape=(32, 32, 3)))
        model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Dropout(0.25))

        model.add(layers.Flatten())
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.BatchNormalization())
        model.add(layers.Dropout(0.5))
        model.add(layers.Dense(9, activation='softmax'))

        model.summary()

        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        early_stopping = EarlyStopping(monitor='val_loss', patience=15, verbose=0, mode='min')
        mcp_save = ModelCheckpoint(checkpoint_path, monitor='val_loss', mode='min', verbose=1,
                                   save_weights_only=True, save_best_only=True)
        reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=10, verbose=1, mode='min')
        model.save_weights(checkpoint_path.format(epoch=0))
        history = model.fit(train_images, train_labels, epochs=20, validation_split=0.2, shuffle=True,
                            batch_size=batch_size, callbacks=[early_stopping, mcp_save, reduce_lr_loss])

        plt.plot(history.history['loss'], label='train_loss')
        plt.plot(history.history['val_loss'], label='validation_loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.ylim([0.5, 1])
        # plt.legend(loc='lower right')
        # plt.show()

    # latest = tf.train.latest_checkpoint(checkpoint_dir)
    # model.load_weights(latest)
    # prediction = model.predict(test_images)
    # new_predictions = []
    # for i in enumerate(prediction):
    #     new_predictions.append(np.argmax(prediction[i]))

    # print(accuracy_score(test_labels, new_predictions))
    # print(classification_report(test_labels, new_predictions, target_names=label_encoder.classes_))


def read_images(all_labels, train_data=True):
    """
    Read in images from directories.
    """

    images = []
    labels = []
    for label in all_labels:
        if train_data:
            path = "./data/train/" + label + "/"
        else:
            path = "./data/test/" + label + "/"
        for filename in os.listdir(path):
            img = cv2.imread(path + "/" + filename)
            if img is not None:
                images.append(img)
                labels.append(label)
    images = np.array(images)
    labels = np.array(labels)
    return images, labels


def find_color_image(x_coord, y_coord, year=2020):
    """
    Find color image.
    """

    # print("COLOR DETECTION RUNNING")
    # path = "./data/parks_detected"
    # shutil.rmtree(path)
    # os.makedirs(path)
    # if download_data:
    #     create_dir(ALL_LABELS)
    #     get_images_training(Classification.objects.filter(year__lte=year), year)
    #     get_images_test(year)

    # train_images = read_images(ALL_LABELS, True)
    # train_labels = read_images(ALL_LABELS, True)
    # test_images = read_images(ALL_LABELS, False)
    # print(train_images.shape)
    # print(test_images.shape)
    # all_images = np.concatenate(train_images, test_images)
    # for i, img in enumerate(train_images):
    img = get_image_from_url(year, x_coord, y_coord)

    if img is None:
        if year >= 2020:
            raise ObjectDoesNotExist("Tile not found.")

        print(year)
        return find_color_image(x_coord, y_coord, year + 1)

    return get_greenery_percentage(img)


def get_greenery_percentage(img):
    """
    Get the percentage of greenery.
    """

    # cv2.imshow("A", img)
    # cv2.waitKey()
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boundaries = [(36, 25, 25), (70, 255, 255)]
    # boundaries = [(37, 0, 0), (179, 255, 255)]
    lower = np.array(boundaries[0], dtype='uint8')
    upper = np.array(boundaries[1], dtype='uint8')
    mask = cv2.inRange(img1, lower, upper)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    opened_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    output = cv2.bitwise_and(img2, img2, mask=opened_mask)
    contours, _ = cv2.findContours(opened_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(output, contours, -1, (0, 255, 0), 1)
    areas = []
    for contour in contours:
        (_, _, w_shape, h_shape) = cv2.boundingRect(contour)
        areas.append(w_shape * h_shape)
        # print(x_shape)
        # print(y_shape)
    if len(areas) > 0:
        # max_area = np.max(areas)
        # if max_area >= 15:
        # cv2.imshow("Image", img2)
        # cv2.waitKey()
        # cv2.imshow("out", output)
        # cv2.waitKey()
        # img_res = np.hstack([img2, output])
        # print(output.shape[0], output.shape[1])
        num_pixels = output.shape[0] * output.shape[1] * output.shape[2]
        # print(num_pixels)
        # print(output)
        non_zero = np.count_nonzero(output)
        # print(non_zero)

        percentage = non_zero / num_pixels
        # print(percentage)
        return percentage

    return 0

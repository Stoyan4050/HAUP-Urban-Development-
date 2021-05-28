"""
Classifier
"""

import urllib.request
import shutil
import os
import cv2
import numpy as np
from django.db.models import Q
from sklearn.decomposition import PCA
from sklearn.metrics import f1_score, classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow.keras import Sequential, layers
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import matplotlib.pyplot as plt
from .models import Classification


ALL_LABELS = ['beach', 'church', 'city square', 'garden', 'greenery', 'museum', 'not a public space',
              'park', 'recreational area']


def get_image_from_url(year, x_coord, y_coord):
    """
        get historic map images from website
    """

    url = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
        year) + "/MapServer/tile/11/" + str(x_coord) + "/" + str(y_coord)

    res = urllib.request.urlretrieve(url)
    img = cv2.resize(cv2.imread(res[0], 1), (32, 32))
    return img


def get_images_training(data, year):
    """
        get images for training
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
        get images for test
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
        random samples
    """

    arr = np.array(arr)
    res = arr[np.random.choice(len(arr), size=int(len(arr)/2), replace=False)]
    return res


def get_labels_imgs(data):
    """
        get labels of images
    """

    labels = []
    imgs = []
    for img, label in data:
        labels.append(label)
        imgs.append(img)
    return np.array(labels), np.array(imgs)


def classify(year=2015, download_data=False):
    """
        classify
    """

    all_labels = ['beach', 'church', 'city square', 'garden', 'greenery', 'museum', 'not a public space', 'park',
                  'recreational area']

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


def tune_hyperparams(estimator_name, estimator, estimator_params, train_labels, train_images):
    """
        tune hyper parameter
    """

    k_fold = KFold(n_splits=12)

    best_model_estimator = Pipeline([("pca", PCA()), (estimator_name, estimator)])
    sum_scores = 0
    best_model_score = 0.0

    vector = np.vectorize(np.int16)

    for train_index, test_index in k_fold.split(train_images):
        x_train, x_test = train_images[vector(train_index)], train_images[vector(test_index)]
        y_train, y_test = train_labels[vector(train_index)], train_labels[vector(test_index)]

        pipe = Pipeline([("pca", PCA()), (estimator_name, estimator)])
        search = GridSearchCV(pipe, estimator_params, cv=5, return_train_score=True, n_jobs=-1, verbose=2,
                              scoring="f1_macro")

        search.fit(x_train, y_train)

        est = search.best_estimator_

        est_pipe = make_pipeline(est)
        est_pipe.fit(x_train, y_train)
        prediction = est_pipe.predict(x_test)

        f1_score_est = f1_score(y_test, prediction, average="macro")

        if f1_score_est > best_model_score:
            best_model_score = f1_score_est
            best_model_estimator = est

        sum_scores = sum_scores + f1_score_est

    mean_score = sum_scores / k_fold.get_n_splits()

    print("Mean score:", mean_score, "\n")
    print("Best score:", best_model_score, "\n")
    print("Best estimator:", best_model_estimator)
    return mean_score, best_model_score, best_model_estimator


def create_dir(all_labels):
    """
        creates directories for storing images. Takes in all labels for directory names
    """

    path_train = "./data/train"
    path_test = "./data/test"
    shutil.rmtree(path_train)
    shutil.rmtree(path_test)
    os.makedirs(path_train)
    os.makedirs(path_test)

    for label in all_labels:
        new_path_train = path_train + "/" + label
        new_path_test = path_test + "/" + label
        os.makedirs(new_path_train)
        os.makedirs(new_path_test)


def save_images(label, img, counter, train=True):
    """
        saves images in corresponding directory. Takes in label for directory, image to store, counter for
        unique file name
    """

    if train:

        path = "./data/train"
        cv2.imwrite(path + "/" + label + "/train_img_" + str(counter) + ".jpg", img)
    else:
        path = "./data/test"
        cv2.imwrite(path + "/" + label + "/test_img_" + str(counter) + ".jpg", img)


def train_cnn(year=2015, download_data=False, train_network=True):
    """
        train Convolutional neural network. Takes in year of map, whether data needs to be downloaded,
        and if network is trained
    """

    if download_data:
        create_dir(ALL_LABELS)
        get_images_training(Classification.objects.filter(year__lte=year), year)
        get_images_test(year)

    train_images, train_labels = read_images(ALL_LABELS, True)
    test_images = read_images(ALL_LABELS, False)
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
    checkpoint_dir = os.path.dirname(checkpoint_path)

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

    latest = tf.train.latest_checkpoint(checkpoint_dir)
    model.load_weights(latest)
    prediction = model.predict(test_images)
    new_predictions = []
    for i in enumerate(prediction):
        new_predictions.append(np.argmax(prediction[i]))
    # print(accuracy_score(test_labels, new_predictions))
    # print(classification_report(test_labels, new_predictions, target_names=label_encoder.classes_))


def read_images(all_labels, train_data=True):
    """
        read in images from directories
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

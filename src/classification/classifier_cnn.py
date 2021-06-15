"""
    classifier_new.py
"""

import numpy as np
import django
import tensorflow as tf
import matplotlib.pyplot as plt
from django.core.exceptions import ObjectDoesNotExist
from keras.optimizer_v2.adam import Adam
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from django.db.models import Q
from api.models import Classification, Tile
import cv2
from . import classifier_svm, classifier


def change_labels(arr):
    """
        changing the labels from True/False to Integers
    """

    new_arr = []
    # print(arr)
    for i in arr:
        if i:
            new_arr.append(1)
        else:
            new_arr.append(0)

    return np.array(new_arr)


def get_training_validation(train_data):
    """
        get training and validaton set
    """

    validation = []
    np.random.shuffle(train_data)
    percent10 = len(train_data) / 10
    counter = 0

    training = []
    for tile, label in train_data:
        counter += 1
        if counter < percent10:
            validation.append((tile, label))
        else:
            training.append((tile, label))

    return np.array(training), np.array(validation)


def get_greenery_percentage(img, year):
    first_colored_map = 1914

    return color_detection_cnn(img, max(year, first_colored_map))


def color_detection_cnn(img, year):
    """
        detect greenery in tiles of maps
    """
    if img is None:
        if year >= 2020:
            raise ObjectDoesNotExist("Tile not found.")

        print(year)
        return color_detection_cnn(img, year + 1)

    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boundaries = [(36, 25, 25), (70, 255, 255)]
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

    if len(areas) > 0:
        num_pixels = output.shape[0] * output.shape[1] * output.shape[2]
        non_zero = np.count_nonzero(output)
        percentage = non_zero / num_pixels
        return percentage

    return 0


def classify_cnn(year=2020):
    """
        classifying using cnn
    """

    training, validation = get_training_validation(np.array(classifier_svm.get_images_training(
        Classification.objects.filter(~Q(classified_by=-1), year__lte=year), year)))

    train_labels, train_images = classifier.get_labels_imgs(training)
    train_labels = change_labels(train_labels)

    val_labels, val_images = classifier.get_labels_imgs(validation)
    val_labels = change_labels(val_labels)

    x_train = np.array(train_images) / 255
    x_val = np.array(val_images) / 255

    img_size = 32
    x_train.reshape((-1, img_size, img_size, 1))
    y_train = np.array(train_labels)

    x_val.reshape((-1, img_size, img_size, 1))
    y_val = np.array(val_labels)

    print(x_train.shape)
    print(x_val.shape)

    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=30,  # randomly rotate images in the range (degrees, 0 to 180)
        zoom_range=0.2,  # Randomly zoom image
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    datagen.fit(x_train)

    model = Sequential()
    model.add(Conv2D(32, 3, padding="same", activation="relu", input_shape=(img_size, img_size, 3)))
    model.add(MaxPool2D())

    model.add(Conv2D(32, 3, padding="same", activation="relu"))
    model.add(MaxPool2D())

    model.add(Conv2D(64, 3, padding="same", activation="relu"))
    model.add(MaxPool2D())
    model.add(Dropout(0.4))

    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dense(2, activation="softmax"))

    model.summary()

    opt = Adam(lr=0.000001)
    model.compile(optimizer=opt, loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, epochs=500, validation_data=(x_val, y_val))

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    epochs_range = range(500)

    plt.figure(figsize=(15, 15))
    plt.subplot(2, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    # plt.show()

    django.db.connections.close_all()
    test_data = classifier_svm.get_images_test(year)
    test_coord, test_images = classifier.get_labels_imgs(test_data)

    predictions = model.predict_classes(test_images)

    for count, prediction in enumerate(predictions):
        class_label = False
        greenery = 0
        tile_x = test_coord[count][1]
        tile_y = test_coord[count][0]

        if prediction == 1:
            class_label = True
            greenery = get_greenery_percentage(test_images[count], year)
            print(greenery)
            # if greenery < 5:
            #     class_label = False

        # print(test_coord[i][1])
        # print(test_coord[i][0])

        # tile_id = tile_x * 75879 + tile_y
        # Classification.objects.create(tile=Tile(tile_id, tile_x, tile_y),
        #                               year=year, greenery_percentage=0,
        #                               contains_greenery=class_label,
        #                               classified_by="-1")

        Classification.objects.create(tile=Tile.objects.get(x_coordinate=tile_x,
                                                            y_coordinate=tile_y),
                                      year=year, greenery_percentage=greenery,
                                      contains_greenery=class_label,
                                      classified_by="-1")
    print(predictions)

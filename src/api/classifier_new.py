from keras.optimizer_v2.adam import Adam
from sklearn.metrics import classification_report

import classifier as cl
import numpy as np
import urllib.request
import django

import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

django.setup()

import cv2

from django.db.models import Q

from .models import Classification, Tile
import tensorflow as tf

def classify_cnn(year=2020):

    train_data = np.array(cl.getImagesTraining(Classification.objects.filter(~Q(classified_by=-1), year__lte=year), year))
    validation = []
    np.random.shuffle(train_data)
    percent10 = train_data / 10
    counter = 0

    training = []
    for f, l in train_data:
        counter+=1
        if counter < percent10:
            validation.append((f,l))
        else:
            training.append((f,l))

    training = np.array(training)
    validation = np.array(validation)

    train_labels, train_images = cl.getLabelsImgs(training)
    val_labels, val_images = cl.getLabelsImgs(validation)

    x_train = np.array(train_images) / 255
    x_val = np.array(val_images) / 255


    y_train = np.array(train_labels)

    m, n, r, k = train_images.shape
    x_train = x_train.reshape(m, n * r * k)
    x_train = np.array(x_train)



    m1, n1, r1, k1 = train_images.shape
    x_val_reshaped = x_val.reshape(m, n * r * k)
    y_val = np.array(val_images)


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
    model.add(Conv2D(32,3,padding="same", activation="relu", input_shape=(224,224,3)))
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
    plt.show()

    print("Training data extracted!")

    predictions = model.predict_classes(x_val)
    predictions = predictions.reshape(1, -1)[0]

    print(classification_report(y_val, predictions, target_names=['Rugby (Class 0)', 'Soccer (Class 1)']))

    # train_images = imgs_train
    django.db.connections.close_all()


    test_data = cl.getImagesTest(year)
    test_coord, test_images = cl.getLabelsImgs(test_data)


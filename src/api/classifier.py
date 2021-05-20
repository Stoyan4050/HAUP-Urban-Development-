import os
import urllib.request

import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from django.db.models import Q
from tensorflow.keras import Sequential
from tensorflow.keras import layers

from .models import Classification, Tile
def getImageFromURL(year, x_coord, y_coord):
    url = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
        year) + "/MapServer/tile/11/" + str(x_coord) + "/" + str(y_coord)

    res = urllib.request.urlretrieve(url)
    img = cv2.resize(cv2.imread(res[0],1), (32,32))
    return img

def getImagesTraining(data, year):
    training_imgs = []
    counter = 0
    for c in data:
        #print(c.year)

        # if tileYear == year:

        tile = c.tile_id
            #print(year)
        img = getImageFromURL(year, tile.y_coordinate, tile.x_coordinate)
            #print(counter)
        training_imgs.append((img, c.label))
        #print(counter)
        print(counter)
        counter+=1
        # if counter > 100:
        #     print(len(training_imgs), "IM")
        #     return training_imgs

    return training_imgs
#
def getImagesTest(year):
    Classification.objects.filter(classified_by=-1).delete()
    data = Classification.objects.filter(~Q(classified_by=-1))
    #print(data)
    # data = Tile.objects.exclude(tid=classified)
    # print(data)
    test_imgs = []
    counter = 0
    for c in data:
        # print(c.year)

        # if tileYear == year:

        tile = c.tile_id
        # print(year)
        img = getImageFromURL(year, tile.y_coordinate, tile.x_coordinate)
        # print(counter)
        coord = (tile.y_coordinate, tile.x_coordinate)
        test_imgs.append((img, coord))
        print(counter)
        counter += 1

    return np.array(test_imgs)


def random_sample(arr):
    arr = np.array(arr)
    #print(arr)
    res = arr[np.random.choice(len(arr), size=int(len(arr)/2), replace=False)]
    return res

# def getPortionOfTheData(data):
#     print(len(data))
#     #np.array(X_train)[indices.astype(int)]
#     ix_size = int(0.05 * len(data))
#     ix = np.random.choice(len(data), size=ix_size, replace=False)
#     train_data_10per = data[ix]
#     np.random.shuffle(train_data_10per)
#     print(len(train_data_10per))
#     return train_data_10per

def getLabelsImgs(data):
    labels = []
    imgs = []
    for img, lb in data:
        labels.append(lb)
        imgs.append(img)
    return np.array(labels), np.array(imgs)

def classify(year=2015):

    train_data = getImagesTraining(Classification.objects.filter(year__lte=year), year)
    #train_data_10per = random_sample(train_data)
    # print(train_data)
    #print(train_data_10per)
    train_labels, train_images = getLabelsImgs(train_data)
    #print(train_labels, train_images)
    print("Training data extracted!")
    # img = getImageFromURL(2020, 75400, 75410)
    # cv2.imshow("img", img)
    # cv2.waitKey()
    imgs_train = []
    # path = "./training_data"
    # valid_images = [".jpg", ".png"]
    # for f in os.listdir(path):
    #     ext = os.path.splitext(f)[1]
    #     if ext.lower() not in valid_images:
    #         continue
    #     imgs_train.append(cv2.imread((os.path.join(path, f)),1))

    imgs_test = []
    # path_test = "./test_data"
    # valid_images = [".jpg", ".png"]
    # for f in os.listdir(path_test):
    #     ext = os.path.splitext(f)[1]
    #     if ext.lower() not in valid_images:
    #         continue
    #     imgs_test.append(cv2.resize((cv2.imread((os.path.join(path_test, f)),1)), (32,32)))

    # train_images = imgs_train
    test_data = getImagesTest(year)
    test_coord, test_images = getLabelsImgs(test_data)

    train_images = np.array(train_images)
    test_images = np.array(test_images)
    #print("TEST", test_images)
    print("Training imgs loaded. Classification starts!")
    m, n, r, k = train_images.shape
    train_imgs_reshaped = train_images.reshape(m, n * r * k)

    # Array that holds the best set of parameters for each model
    best_estimators = np.empty(0)

    # Array that holds the mean score obtained during hyperparamter tuning for each model
    hyperparameter_tuning_scores = np.empty(0)

    # Array containing the score of the highest rated estimator for each model
    # best_scores = np.empty(0)

    models = {
        "KNeighborsClassifier": KNeighborsClassifier(n_neighbors=3, weights="distance"),
        "SVM": SVC(C=10, kernel="poly", random_state=42),
        "DecisionTreeClassifier": DecisionTreeClassifier(max_depth=None, min_samples_leaf=2, random_state=42),
        "LogisticRegression": LogisticRegression(C=10, random_state=42, penalty="none", max_iter=1000)

    }
    params = [
        {
            "pca__n_components": np.linspace(0.5, 0.99, 2),
            "svm__C": np.arange(start=1, stop=10, step=2),
            "svm__kernel": ["poly", "sigmoid"],
            "svm__random_state": [42]
        }
    ]

    mean_score, best_model_score, best_model_estimator = tune_hyperparams("svm",
                                                                          models["SVM"],
                                                                          params, train_labels, train_imgs_reshaped)

    hyperparameter_tuning_scores = np.append(hyperparameter_tuning_scores, mean_score)
    best_estimators = np.append(best_estimators, best_model_estimator)
    # best_scores = np.append(best_scores, best_model_score)

    # print(hyperparameter_tuning_scores, "ddd")
    # print(best_estimators, "ccc")
    # print(best_scores, "bb")

    mte, nte, rte, kte = test_images.shape
    test_imgs_reshaped = test_images.reshape(mte, nte * rte * kte)
    #print("After reshaping " + str(test_imgs_reshaped.shape))

    # best_model = best_estimators[np.argmax(hyperparameter_tuning_scores)]
    pipe = make_pipeline(best_estimators[0], best_estimators[1])
    pipe.fit(train_imgs_reshaped, train_labels)
    prediction = pipe.predict(test_imgs_reshaped)
    print(best_estimators)
    print(prediction)

    print(test_coord)
    for i in range(len(prediction)):
        print(test_coord[i][1])
        print(test_coord[i][0])
        Classification.objects.create(tile_id=Tile.objects.get(x_coordinate=test_coord[i][1], y_coordinate=test_coord[i][0]), year=year, label=prediction[i], classified_by="-1")
        #Classification.objects.filter(tile_id=Tile.objects.get(x_coordinate=test_coord[i][1], y_coordinate=test_coord[i][0]).tid).update(year=year, label=prediction[i], classified_by="-1")

def tune_hyperparams(estimator_name, estimator, estimator_params, train_labels, train_images):

    k_fold = KFold(n_splits=12)


    best_model_estimator = Pipeline([("pca", PCA()), (estimator_name, estimator)])
    sum_scores = 0
    best_model_score = 0.0
    # print(len(train_labels))
    # print(len(train_images))
    vector = np.vectorize(np.int16)

    for train_index, test_index in k_fold.split(train_images):
        # print(train_index)
        Xtrain, Xtest = train_images[vector(train_index)], train_images[vector(test_index)]
        Ytrain, Ytest = train_labels[vector(train_index)], train_labels[vector(test_index)]

        pipe = Pipeline([("pca", PCA()), (estimator_name, estimator)])
        search = GridSearchCV(pipe, estimator_params, cv=5, return_train_score=True, n_jobs=-1, verbose=2,
                                  scoring="f1_macro")

        search.fit(Xtrain, Ytrain)

        est = search.best_estimator_
        # print("ESST", est)
        # print("BESST", search.best_score_)

        est_pipe = make_pipeline(est)
        est_pipe.fit(Xtrain, Ytrain)
        prediction = est_pipe.predict(Xtest)

        f1_score_est = f1_score(Ytest, prediction, average="macro")
        # print("f1_score_: ", f1_score_est)

        if (f1_score_est > best_model_score):
            best_model_score = f1_score_est
            best_model_estimator = est

        sum_scores = sum_scores + f1_score_est

    mean_score = sum_scores / k_fold.get_n_splits()


    # print("Mean score:", mean_score, "\n")
    # print("Best score:", best_model_score, "\n")
    # print("Best estimator:", best_model_estimator)
    return mean_score, best_model_score, best_model_estimator




    #------------------------------ TensorFlow approach - in progress:
def train_cnn(year=2015):
    train_data = getImagesTraining(Classification.objects.filter(year__lte=year), year)
    # train_data_10per = random_sample(train_data)
    # print(train_data)
    # print(train_data_10per)
    train_labels, train_images = getLabelsImgs(train_data)
    # print(train_labels, train_images)
    print("Training data extracted!")

    test_data = getImagesTest(year)
    test_coord, test_images = getLabelsImgs(test_data)

    train_images = np.array(train_images)
    test_images = np.array(test_images)
    # print("TEST", test_images)
    print("Training imgs loaded. Classification starts!")



    # Normalize pixel values to be between 0 and 1
    train_images, test_images = train_images / 255.0, test_images / 255.0

    model = Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))



    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10))

    model.summary()

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(train_images, train_labels, epochs=5,
                     validation_split=0.2)

    plt.plot(history.history['accuracy'], label='accuracy')
    plt.plot(history.history['val_accuracy'], label='val_accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.ylim([0.5, 1])
    plt.legend(loc='lower right')
    plt.show()
    #test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    prediction = model.predict(test_images)
    print(prediction)
    #print(test_acc)
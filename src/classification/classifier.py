"""
classifier.py
"""

import os
import cv2
import numpy as np
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


def classify():
    """
    def classify()
    """

    imgs_train = []
    path = "./training_data"
    valid_images = [".jpg", ".png"]
    
    for file in os.listdir(path):
        ext = os.path.splitext(file)[1]
        
        if ext.lower() not in valid_images:
            continue
        
        imgs_train.append(cv2.imread((os.path.join(path, file)), 1))

    imgs_test = []
    path_test = "./test_data"
    valid_images = [".jpg", ".png"]
    
    for file in os.listdir(path_test):
        ext = os.path.splitext(file)[1]
        
        if ext.lower() not in valid_images:
            continue
        
        imgs_test.append(cv2.imread((os.path.join(path_test, file)), 1))

    train_images = imgs_train
    test_images = imgs_test
    train_labels = ["park", "park", "park", "park", "park", "park", "park", "park", "no-park",
                    "no-park", "no-park", "no-park", "no-park", "no-park", "no-park", "no-park", ]

    train_images = np.array(train_images)
    test_images = np.array(test_images)
    print(train_images.shape)
    count, height, width, channels = train_images.shape
    train_imgs_reshaped = train_images.reshape(count, height * width * channels)
    train_labels = np.array(train_labels)

    # Array that holds the best set of parameters for each model
    best_estimators = np.empty(0)

    # Array that holds the mean score obtained during hyperparamter tuning for each model
    # hyperparameter_tuning_scores = np.empty(0)

    # Array containing the score of the highest rated estimator for each model
    # best_scores = np.empty(0)

    models = {
        "KNeighborsClassifier": KNeighborsClassifier(n_neighbors=3, weights="distance"),
        "SVM": SVC(C=10, kernel="poly", random_state=42),
        "DecisionTreeClassifier": DecisionTreeClassifier(max_depth=None, min_samples_leaf=2, random_state=42),
        "LogisticRegression": LogisticRegression(C=10, random_state=42, penalty="none", max_iter=1000),
    }
    params = [
        {
            "pca__n_components": np.linspace(0.5, 0.99, 2),
            "svm__C": np.arange(start=1, stop=10, step=2),
            "svm__kernel": ["poly", "sigmoid"],
            "svm__random_state": [42],
        }
    ]

    _, _, best_model_estimator = tune_hyperparams("svm", models["SVM"], params, train_imgs_reshaped, train_labels)

    # hyperparameter_tuning_scores = np.append(hyperparameter_tuning_scores, mean_score, )
    best_estimators = np.append(best_estimators, best_model_estimator)
    # best_scores = np.append(best_scores, best_model_score)

    # print(hyperparameter_tuning_scores, "ddd")
    # print(best_estimators, "ccc")
    # print(best_scores, "bb")

    mte, nte, rte, kte = test_images.shape
    test_imgs_reshaped = test_images.reshape(mte, nte * rte * kte)
    # print("After reshaping " + str(test_imgs_reshaped.shape))

    # best_model = best_estimators[np.argmax(hyperparameter_tuning_scores)]
    pipe = make_pipeline(best_estimators[0], best_estimators[1])
    pipe.fit(train_imgs_reshaped, train_labels)
    prediction = pipe.predict(test_imgs_reshaped)
    print(prediction)


def tune_hyperparams(estimator_name, estimator, estimator_params, train_images, train_labels):
    """
    def tune_hyperparams(estimator_name, estimator, estimator_params, train_images, train_labels)
    """

    k_fold = KFold(n_splits=4)
    best_model_estimator = Pipeline([("pca", PCA()), (estimator_name, estimator)])
    sum_scores = 0
    best_model_score = 0.0

    for train_index, test_index in k_fold.split(train_images):
        x_train, x_test = train_images[train_index], train_images[test_index]
        y_train, y_test = train_labels[train_index], train_labels[test_index]

        pipe = Pipeline([("pca", PCA()), (estimator_name, estimator)])
        search = GridSearchCV(pipe, estimator_params, cv=5, return_train_score=True, n_jobs=-1, verbose=2,
                              scoring="f1_macro")

        search.fit(x_train, y_train)

        est = search.best_estimator_
        # print("ESST", est)
        # print("BESST", search.best_score_)

        est_pipe = make_pipeline(est)
        est_pipe.fit(x_train, y_train)
        prediction = est_pipe.predict(x_test)

        f1_score_est = f1_score(y_test, prediction, average="macro")
        # print("f1_score_: ", f1_score_est)

        if f1_score_est > best_model_score:
            best_model_score = f1_score_est
            best_model_estimator = est

        sum_scores = sum_scores + f1_score_est

    mean_score = sum_scores / k_fold.get_n_splits()

    # print("Mean score:", mean_score, "\n")
    # print("Best score:", best_model_score, "\n")
    # print("Best estimator:", best_model_estimator)

    return mean_score, best_model_score, best_model_estimator

    # ------------------------------ TensorFlow approach - in progress:
    #
    # # Normalize pixel values to be between 0 and 1
    # train_images, test_images = train_images / 255.0, test_images / 255.0
    #
    # model = models.Sequential()
    # model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
    # model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    # model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    #
    # model.summary()
    #
    # model.add(layers.Flatten())
    # model.add(layers.Dense(64, activation='relu'))
    # model.add(layers.Dense(10))
    #
    # model.compile(optimizer='adam',
    #               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    #               metrics=['accuracy'])
    #
    # # history = model.fit(train_images, train_labels, epochs=5,
    # #                     validation_data=(test_images, test_labels))
    # #
    # # plt.plot(history.history['accuracy'], label='accuracy')
    # # plt.plot(history.history['val_accuracy'], label='val_accuracy')
    # # plt.xlabel('Epoch')
    # # plt.ylabel('Accuracy')
    # # plt.ylim([0.5, 1])
    # # plt.legend(loc='lower right')
    # # plt.show()
    # #test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    # prediction = model.predict(test_images)
    # print(prediction)
    # #print(test_acc)

"""
classifier.py
"""
import urllib.request
import django


django.setup()

import cv2
import numpy as np

from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV, train_test_split, cross_val_score
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from django.db.models import Q

from .models import Classification, Tile

#global data, year

def getImageFromURL(year, x_coord, y_coord):
    print(year, x_coord, y_coord, "DATA")
    url = "https://tiles.arcgis.com/tiles/nSZVuSZjHpEZZbRo/arcgis/rest/services/Historische_tijdreis_" + str(
        year) + "/MapServer/tile/11/" + str(x_coord) + "/" + str(y_coord)

    res = urllib.request.urlretrieve(url)
    img = cv2.resize(cv2.imread(res[0],1), (32,32))
    return img


def getImgsURL(i, year, data):
    #print(params.data)
    c = data[i]

    tile = c.tile_id
        #print(year)
    img = getImageFromURL(year, tile.y_coordinate, tile.x_coordinate)
        #print(counter)
    #return img
    # print("Y")
    return (img, c.greenery_percentage)

def getImagesTraining(data1, year):
    first = 0
    data = data1
    training_imgs = []
    counter = 0
    print("Taking images", year, data)
    for i in range(len(data)):
        training_imgs.append(getImgsURL(i, year, data))
        print(counter)
        counter+=1

        if counter > 100:
            return training_imgs

    return training_imgs
    #     print(i)
    #     p = Process(target=getImgsURL, args=(i, ))
    #     processes.append(p)
    #     p.start()
    #
    # for process in processes:
    #     process.join()



    # pool = multiprocessing.Pool()
    # pool.map(getImgsURL, range(0, len(data)))
    # pool.close()
    # for i in range(0, len(data)):
    #     #print(c.year)
    #
    #     # if tileYear == year:
    #     c = data[i]
    #     tile = c.tile_id
    #         #print(year)
    #     img = getImageFromURL(year, tile.y_coordinate, tile.x_coordinate)
    #         #print(counter)
    #     training_imgs.append((img, c.label))
        #print(counter)
    # print(counter)
    # counter+=1
    # if counter > 100:
    #     #print(len(training_imgs), "IM")
    #     return training_imgs

    # return training_imgs
#
def getImagesTest(year):
    #Classification.objects.filter(classified_by=-1).delete()
    data_temp = Classification.objects.values("tile_id").distinct()
    data = Tile.objects.filter(~Q(tid__in=data_temp.values_list("tile_id", flat=True)))
    #print(data)
    # data = Tile.objects.exclude(tid=classified)
    # print(data)
    test_imgs = []
    counter = 0
    for tile in data[111111:]:
        # print(c.year)

        # if tileYear == year:
        #if counter > 100000 and counter < 105000:
        # print(year)
        img = getImageFromURL(year, tile.y_coordinate, tile.x_coordinate)
        # print(counter)
        coord = (tile.y_coordinate, tile.x_coordinate)
        test_imgs.append((img, coord))
        #print(counter)

        if counter > 8888:
            break

        #print(counter)
        counter+=1

    return test_imgs


def random_sample(arr):
    arr = np.array(arr)
    #print(arr)
    res = arr[np.random.choice(len(arr), size=int(len(arr)/2), replace=False)]
    return res


def getLabelsImgs(data):
    labels = []
    imgs = []
    for img, lb in data:
        labels.append(lb)
        imgs.append(img)
    return np.array(labels), np.array(imgs)

def classify(year=2020):

    #train_data = getImagesTraining(Classification.objects.filter(year__lte=year), year)
    # classifier_params.data_selected = []
    # classifier_params.year_selected = 2020
    # classifier_params.train_data_imgs = []
    # classifier_params.global_counter = 0
    #params = classifier_params(year, data=[], counter=0)
    train_data = np.array(getImagesTraining(Classification.objects.filter(~Q(classified_by=-1), year__lte=year), year))

    #train_data_10per = random_sample(train_data)
    # print(train_data)
    #print(train_data_10per)
    train_labels, train_images = getLabelsImgs(train_data)
    #print(train_images, "imgs")

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
    django.db.connections.close_all()
#    django.db.connections.execute('set max_allowed_packet=67108864')

    test_data = getImagesTest(year)
    test_coord, test_images = getLabelsImgs(test_data)

   # print(test_images)
    train_images = np.array(train_images)
    test_images = np.array(test_images)
    #print("TEST", test_images)
    print("Training imgs loaded. Classification starts!")
    #print(train_images)
    m, n, r, k = train_images.shape

    train_imgs_reshaped = train_images.reshape(m, n * r * k)

    # Array that holds the best set of parameters for each model
    best_estimators = np.empty(0)

    # Array that holds the mean score obtained during hyperparamter tuning for each model
    hyperparameter_tuning_scores = np.empty(0)

    # Array containing the score of the highest rated estimator for each model
    best_scores = np.empty(0)

    names = {"KNeighborsClassifier", "SVM", "SVM_Tuned", "DecisionTreeClassifier", "LogisticRegression"}
    models = {
        "KNeighborsClassifier": KNeighborsClassifier(n_neighbors=3, weights="distance"),
        "SVM": SVC(C=10, kernel="poly", random_state=42),
        "SVM_Tuned": SVC(C=7, kernel="poly", random_state=42),
        "DecisionTreeClassifier": DecisionTreeClassifier(max_depth=None, min_samples_leaf=2, random_state=42),
        "LogisticRegression": LogisticRegression(C=10, random_state=42, penalty="none", max_iter=1000)

    }
    params = [
        {
            "pca__n_components": np.linspace(0.5, 0.99, 4),
            "svm__C": np.arange(start=1, stop=20, step=4),
            "svm__kernel": ["poly", "rbf", "sigmoid"],
            "svm__random_state": [42]
        }
    ]

    #mean_score, best_model_score, best_model_estimator = tune_hyperparams("svm",
    #                                                                       models["SVM"],
    #                                                                       params, train_labels, train_imgs_reshaped)

    # hyperparameter_tuning_scores = np.append(hyperparameter_tuning_scores, mean_score)
    # best_estimators = np.append(best_estimators, best_model_estimator)
    # best_scores = np.append(best_scores, best_model_score)

    print(hyperparameter_tuning_scores, "- Hyper_Parameter_Tuning_Scores")
    print(best_estimators, "- Best Estimator")
    print(best_scores, "Best scores")

    mte, nte, rte, kte = test_images.shape
    test_imgs_reshaped = test_images.reshape(mte, nte * rte * kte)
    #print("After reshaping " + str(test_imgs_reshaped.shape))

    best_model = best_estimators[np.argmax(hyperparameter_tuning_scores)]

    #pipe = Pipeline([("pca", PCA(0.99)), ("SVM_Tuned", models["SVM_Tuned"])])

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(train_images, train_labels, test_size=0.4, random_state=42,
                                                    shuffle=True, stratify=train_images)

    m, n, r, k = train_images.shape

    train_imgs_reshaped = train_images.reshape(m, n * r * k)

    Xtrain2D = Xtrain.reshape(m, n * r * k)
    Xtest2D = Xtest.reshape(m, n * r * k)
    for name, model in models.items():
        print(name)
        model.fit(Xtrain2D, Ytrain)

    from sklearn.metrics import f1_score, accuracy_score
    names = np.empty(0)
    scores = np.empty(0)
    meanErrors = np.empty(0)

    for name, model in models.items():
        prediction = model.predict(Xtest2D)
        f1_score_value = f1_score(Ytest, prediction, average="weighted")
        print(name)
        print("- f1_score", f1_score_value)
        names = np.append(names, name)
        scores = np.append(scores, f1_score_value)

        score = cross_val_score(model, Xtrain2D, Ytrain, cv=10)
        meanErrors = np.append(meanErrors, np.mean(score))
        print(score)

    pipe = make_pipeline(best_estimators[0], best_estimators[1])
    #pipe.fit(train_imgs_reshaped, train_labels)
    prediction = pipe.predict(test_imgs_reshaped)
    #print(best_estimators)
    print(prediction)

    print(test_coord)
    django.db.connections.close_all()
    #django.db.connections.execute('set max_allowed_packet=67108864')
    for i in range(len(prediction)):
        #print(test_coord[i][1])
        #print(test_coord[i][0])
        Classification.objects.create(tile_id=Tile.objects.get(x_coordinate=test_coord[i][1], y_coordinate=test_coord[i][0]), year=year, label=prediction[i], classified_by="-1")
        #Classification.objects.filter(tile_id=Tile.objects.get(x_coordinate=test_coord[i][1], y_coordinate=test_coord[i][0]).tid).update(year=year, label=prediction[i], classified_by="-1")

def tune_hyperparams(estimator_name, estimator, estimator_params, train_labels, train_images):

    #print(train_images)
    #print(train_labels)
    k_fold = KFold(n_splits=3)


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


    print("Mean score:", mean_score, "\n")
    print("Best score:", best_model_score, "\n")
    print("Best estimator:", best_model_estimator)
    return mean_score, best_model_score, best_model_estimator

class classifier_params:
    year = 2020
    counter = 0
    train_imgs = []
    data = []

    def __init__(self, year, data, counter):
        self.year_selected = year
        self.data = data
        self.counter = counter






    #------------------------------ TensorFlow approach - in progress:
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

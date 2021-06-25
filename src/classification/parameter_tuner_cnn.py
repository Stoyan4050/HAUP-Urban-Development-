"""
parameter_tuner_cnn.py
"""

import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from kerastuner import Hyperband


def model_builder(hyper):
    """
    Build a model for hyperparameter tuning.
    """

    # model = keras.Sequential()
    # model.add(keras.layers.Flatten(input_shape=(28, 28)))
    #
    # Tune the number of units in the first Dense layer
    # Choose an optimal value between 32-512
    # hp_units = hp.Int('units', min_value=32, max_value=512, step=32)
    # model.add(keras.layers.Dense(units=hp_units, activation='relu'))
    # model.add(keras.layers.Dense(10))

    # Tune the learning rate for the optimizer
    # Choose an optimal value from 0.01, 0.001, or 0.0001
    hp_learning_rate = hyper.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4, 0.000001, 0.00001])

    img_size = 32
    model = Sequential()
    model.add(Conv2D(
        filters=hyper.Choice(
            'num_filters',
            values=[32, 48, 64, 80, 96, 112, 128],
            default=64,
        ),
        activation='relu',
        kernel_size=3,
        padding="same",
        input_shape=(img_size, img_size, 3)
    ))

    # Conv2D(32, 3, padding="same", activation="relu", input_shape=(img_size, img_size, 3))
    model.add(MaxPool2D())

    model.add(Conv2D(filters=hyper.Choice('num_filters',
                                          values=[32, 48, 64, 80, 96, 112, 128],
                                          default=64),
                     kernel_size=3,
                     padding="same",
                     activation="relu"))

    model.add(MaxPool2D())

    model.add(Conv2D(filters=hyper.Choice(
        'num_filters',
        values=[32, 48, 64, 80, 96, 112, 128],
        default=64),
                     kernel_size=3,
                     padding="same",
                     activation="relu"))

    model.add(MaxPool2D())

    model.add(Dropout(
        rate=hyper.Float(
            'dropout_3',
            min_value=0.0,
            max_value=0.7,
            default=0.4,
            step=0.1
        )
    ))

    model.add(Flatten())

    model.add(Dense(
        units=hyper.Int(
            'units',
            min_value=2,
            max_value=512,
            step=2,
            default=128
        ),
        activation=hyper.Choice(
            'dense_activation',
            values=['relu', 'tanh', 'sigmoid', 'softmax'],
            default='relu'
        )
    ))

    model.add(Dense(
        units=hyper.Int(
            'units',
            min_value=2,
            max_value=512,
            step=2,
            default=2
        ),
        activation=hyper.Choice(
            'dense_activation',
            values=['relu', 'tanh', 'sigmoid', 'softmax'],
            default='relu'
        )
    ))

    opt = Adam(learning_rate=hp_learning_rate)
    model.compile(optimizer=opt,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def paramter_tuning_cnn(img_train, label_train, img_test, label_test):
    """
    Perform hyperparameter tuning.
    """

    tuner = Hyperband(model_builder,
                      objective='val_accuracy',
                      max_epochs=50,
                      factor=3)

    stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

    tuner.search(img_train, label_train, epochs=50, validation_split=0.2, callbacks=[stop_early])

    # Get the optimal hyperparameters
    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

    model = tuner.hypermodel.build(best_hps)
    history = model.fit(img_train, label_train, epochs=50, validation_split=0.2)

    val_acc_per_epoch = history.history['val_accuracy']
    best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1
    print('Best epoch: %d' % (best_epoch,))

    hypermodel = tuner.hypermodel.build(best_hps)

    # Retrain the model
    history = hypermodel.fit(img_train, label_train, epochs=best_epoch, validation_split=0.2)

    eval_result = hypermodel.evaluate(img_test, label_test)
    print("[test loss, test accuracy]:", eval_result)

    return hypermodel, history

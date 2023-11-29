import keras
import numpy as np
import os
from consts import SCREEN_SIZE


def matrix_flip(a):
    m = [[0] * SCREEN_SIZE for i in range(SCREEN_SIZE)]
    for x in range(SCREEN_SIZE):
        for y in range(SCREEN_SIZE):
            m[x][y] = a[y][x]

    return m


class AiModel:

    def __init__(self):
        self.model = self.create_model()
        self.checkpoint_path = 'training_1/cp.ckpt'
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)
        self.loaded = False

    def create_model(self):
        self.model = keras.Sequential()
        self.model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(SCREEN_SIZE, SCREEN_SIZE, 1)))
        self.model.add(keras.layers.MaxPool2D((2, 2)))
        self.model.add(keras.layers.Conv2D(64, (3, 3), activation='relu', ))
        self.model.add(keras.layers.MaxPool2D((2, 2)))
        self.model.add(keras.layers.Conv2D(64, (3, 3), activation='relu', ))
        self.model.add(keras.layers.MaxPool2D((2, 2)))

        self.model.add(keras.layers.Flatten())
        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Dense(10))

        self.model.compile(
            optimizer='adam',
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        return self.model

    def save_model(self):
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

        x_train = x_train / 255.0
        x_test = x_test / 255.0

        # self.model = self.create_model()

        cp_callback = keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path, save_weights_only=True, verbose=1)

        history = self.model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test), callbacks=[cp_callback])
        self.loaded = True
        print("LOADED!")
        return self.model

    def load_model(self):
        os.listdir(self.checkpoint_dir)
        self.model.load_weights(self.checkpoint_path)

        # loss, acc = model.evaluate(x_test, y_test, verbose=2)
        self.loaded = True
        print("LOADED!")
        return self.model

    def predict(self, grid):
        model = self.load_model()
        grid_flipped = matrix_flip(grid)

        img = np.expand_dims(grid_flipped, axis=0)
        prediction = model.predict_on_batch(img)
        max_index = 0
        for i in range(10):
            if prediction[0][max_index] < prediction[0][i]:
                max_index = i

        print(max_index)

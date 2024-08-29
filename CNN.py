# -*- coding: utf-8 -*-
"""GROUP_11.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1PCYbcPcdciFP_yAT224lurmA1J29FrCV
"""

import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import numpy as np

(X_train, y_train), (X_test,y_test) = datasets.cifar10.load_data()
#y is a 2D array, for any classification, a 1D array is enough
y_train = y_train.reshape(-1,)
y_test = y_test.reshape(-1,)
classes = ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

# prompt: create a function that plots a sample with the X and y of a training data given the index

import matplotlib.pyplot as plt
def plot_sample(X, y, index):
  plt.figure(figsize = (10,1))
  plt.imshow(X[index])
  plt.xlabel(classes[y[index]])

# prompt: normalise the X_train and X_test
X_train = X_train.astype('float32') / 255.0
X_test = X_test.astype('float32') / 255.0

# prompt: build a convolutional neural network to train the X
from tensorflow.keras import optimizers

model_cnn = models.Sequential()
model_cnn.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model_cnn.add(layers.MaxPooling2D((2, 2)))
model_cnn.add(layers.Conv2D(64, (3, 3), activation='relu'))
model_cnn.add(layers.MaxPooling2D((2, 2)))
model_cnn.add(layers.Conv2D(64, (3, 3), activation='relu'))
model_cnn.add(layers.Flatten())
model_cnn.add(layers.Dense(64, activation='relu'))
model_cnn.add(layers.Dense(10, activation='softmax'))

custom_optimizer = optimizers.Adam(learning_rate=0.001) # tried with optimizer.SGD too and lr=0.01 and lr=0.005 for the respective optimizers
model_cnn.compile(optimizer=custom_optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# prompt: plot the loss over the training epochs

import matplotlib.pyplot as plt
adam_001 = model_cnn.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test)) # tried with batch_size=16 and batch_size=64

# Get the loss values from the history dictionary
loss = adam_001.history['loss']
val_loss = adam_001.history['val_loss']

# Get the number of epochs
epochs = range(1, len(loss) + 1)

# Plot the loss and validation loss over epochs
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# prompt: give me the prediction of y with X_test using model_cnn
y_pred_cnn = model_cnn.predict(X_test)

y_pred_classes_cnn = [np.argmax(element) for element in y_pred_cnn]

from sklearn.metrics import classification_report

print(classification_report(y_test, y_pred_classes_cnn))
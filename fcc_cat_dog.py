# -*- coding: utf-8 -*-
"""fcc_cat_dog.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18shziM3abzzNrJBwKFJ6Mnr71Ve8eCO7
"""

# Commented out IPython magic to ensure Python compatibility.


import tensorflow as tf

from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Input # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator # type: ignore

import requests
import zipfile
import os
import numpy as np
import matplotlib.pyplot as plt


# Get project files
'''
url = "https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip"
file_name = "cats_and_dogs.zip"
response = requests.get(url)

with open(file_name, "wb") as file:
  file.write(response.content)

# Unzip the file
with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall("cats_and_dogs")

# Optionally, remove the zip file after extraction
os.remove(file_name)
'''


PATH = 'Cat and Dog Image Classifier\cats_and_dogs'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')


# Get number of files in each directory. The train and validation directories
# each have the subdirecories "dogs" and "cats".

total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

# Variables for pre-processing and training.
batch_size = 128
epochs = 15
IMG_HEIGHT = 150
IMG_WIDTH = 150


# 3
train_image_generator = ImageDataGenerator(rescale=1./255)
validation_image_generator = ImageDataGenerator(rescale=1./255)
test_image_generator = ImageDataGenerator(rescale=1./255)

train_data_gen = train_image_generator.flow_from_directory(
    directory= train_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size= batch_size,
    class_mode='binary'
)

val_data_gen = validation_image_generator.flow_from_directory(
    directory= validation_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=batch_size,
    class_mode='binary'
)

test_data_gen = test_image_generator.flow_from_directory(
    directory= test_dir,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=1,
    class_mode=None,
    shuffle = False
)

# 4



def plotImages(images_arr, probabilities = False):
  fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
  if probabilities is False:
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
  else:
    for img, probability, ax in zip( images_arr, probabilities, axes):
        ax.imshow(img)
        ax.axis('off')
        if probability > 0.5:
            ax.set_title("%.2f" % (probability*100) + "% dog")
        else:
            ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
  plt.show()

sample_training_images, _ = next(train_data_gen)
# )


# 5
'''train_image_generator = ImageDataGenerator(
   rescale=1./255,
   rotation_range=45,
   width_shift_range=0.1,
   height_shift_range=0.1,
   shear_range=0.1,
   zoom_range=0.1,
   horizontal_flip=True
   )'''


# 6
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size, directory=train_dir,target_size=(IMG_HEIGHT, IMG_WIDTH), class_mode='binary')
augmented_images = [train_data_gen[0][0][0] for i in range(5)]

#plotImages(augmented_images)


# 7
model = Sequential()

model.add(Input(shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.summary()

# Compile the model with a lower learning rate
from tensorflow.keras.optimizers import Adam # type: ignore
optimizer = Adam(learning_rate=0.0001)  # Lower learning rate

model.compile(optimizer="Adam",loss='binary_crossentropy',metrics=['accuracy'])

# 8
steps_per_epoch = int(np.ceil(total_train / batch_size))
validation_steps = int(np.ceil(total_val / batch_size))
history = model.fit(train_data_gen, epochs=epochs, validation_data=val_data_gen)


# 9
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']
print(acc, loss)
print(val_acc, val_loss)

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

#10

predictions = model.predict(test_data_gen)
probs = predictions.flatten()
probabilities = (probs > 0.5).astype("int32")
print(probabilities)



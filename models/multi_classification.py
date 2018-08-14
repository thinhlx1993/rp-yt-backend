# -*- coding: utf-8 -*-
import tensorflow as tf
tf.__version__
import sys
import os
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, Activation
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras import callbacks
from livelossplot import PlotLossesKeras

train_data_path = './dataset/training_set'
validation_data_path = './dataset/test_set'

"""
Parameters
"""
img_width, img_height = 150, 150
batch_size = 32
nb_train_samples = 3946
nb_validation_samples = 642
samples_per_epoch = 8000
validation_steps = 300
nb_filters1 = 32
nb_filters2 = 64
conv1_size = 3
conv2_size = 2
pool_size = 2
classes_num = 5
lr = 1e-4
momentum = 0.9
epochs = 25

model = Sequential()
model.add(Convolution2D(nb_filters1, conv1_size, conv1_size, border_mode ="same", input_shape=(img_width, img_height, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size)))

model.add(Convolution2D(nb_filters2, conv2_size, conv2_size, border_mode ="same"))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(pool_size, pool_size), dim_ordering='th'))

model.add(Flatten())
model.add(Dense(256))
model.add(Activation("relu"))
model.add(Dropout(0.5))
model.add(Dense(classes_num, activation='softmax'))

#model.compile(loss='categorical_crossentropy',
#              optimizer=optimizers.SGD(lr=lr, momentum=momentum),
#              metrics=['accuracy'])

model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=lr),
              metrics=['accuracy'])

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
    validation_data_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

"""
Tensorboard log
"""
#log_dir = './tf-log/'
#tb_cb = callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
#cbks = [tb_cb]

model.fit_generator(
    train_generator,
    steps_per_epoch=2104,
    epochs=epochs,
    validation_data=validation_generator,
    callbacks=[PlotLossesKeras()],
    validation_steps=492)

target_dir = './models/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
model.save('./models/model.h5')
model.save_weights('./models/weights.h5')

print(train_generator.class_indices)
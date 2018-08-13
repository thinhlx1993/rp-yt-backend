# -*- coding: utf-8 -*-

import os
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model

img_width, img_height = 150, 150
model_path = './models/model.h5'
model_weights_path = './models/weights.h5'
model = load_model(model_path)
model.load_weights(model_weights_path)

def predict(file):
    x = load_img(file, target_size=(img_width,img_height))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = model.predict(x)
    result = array[0]
    answer = np.argmax(result)
#    print(answer)
#    if answer == 0:
#        print("Label: bicycles")
#    elif answer == 1:
#        print("Labels: bridges")
#    elif answer == 2:
#        print("Label: bus")
#    elif answer == 3:
#        print("Label: motorcycles")
#    elif answer == 4:
#        print("Label: mountains_or_hills")
#    elif answer == 5:
#        print("Label: statues")
#    elif answer == 6:
#        print("Label: storefront")

    return answer

bicycles_t = 0
bicycles_f = 0
bridges_t = 0
bridges_f = 0
bus_t = 0
bus_f = 0
motorcycles_t = 0
motorcycles_f = 0
mountains_or_hills_t = 0
mountains_or_hills_f = 0
statues_t = 0
statues_f = 0
storefront_t = 0
storefront_f = 0

for i, ret in enumerate(os.walk('./dataset/test_set/bicycles')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: bicycles")
    result = predict(ret[0] + '/' + filename)
    if result == 0:
      bicycles_t += 1
    else:
      bicycles_f += 1

for i, ret in enumerate(os.walk('./dataset/test_set/bridges')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: bridges")
    result = predict(ret[0] + '/' + filename)
    if result == 1:
      bridges_t += 1
    else:
      bridges_f += 1

for i, ret in enumerate(os.walk('./dataset/test_set/bus')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: bus")
    result = predict(ret[0] + '/' + filename)
    if result == 1:
      bus_t += 1
    else:
      bus_f += 1

for i, ret in enumerate(os.walk('./dataset/test_set/motorcycles')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: motorcycles")
    result = predict(ret[0] + '/' + filename)
    if result == 2:
      motorcycles_t += 1
    else:
      motorcycles_f += 1

for i, ret in enumerate(os.walk('./dataset/test_set/mountains_or_hills')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: mountains_or_hills")
    result = predict(ret[0] + '/' + filename)
    if result == 4:
      mountains_or_hills_t += 1
    else:
      mountains_or_hills_f += 1

for i, ret in enumerate(os.walk('./dataset/test_set/statues')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: statues")
    result = predict(ret[0] + '/' + filename)
    if result == 5:
      statues_t += 1
    else:
      statues_f += 1
    
for i, ret in enumerate(os.walk('./dataset/test_set/storefront')):
  for i, filename in enumerate(ret[2]):
    if filename.startswith("."):
      continue
#    print("Label: storefront")
    result = predict(ret[0] + '/' + filename)
    print(result)
    if result == 6:
      storefront_t += 1
    else:
      storefront_f += 1
"""
Check metrics
"""
print("True bicycles: ", bicycles_t)
print("False bicycles: ", bicycles_f)
print("True bus: ", bus_t)
print("False bus: ", bus_f)
print("True motorcycles: ", motorcycles_t)
print("False motorcycles: ", motorcycles_f)
print("True bridges: ", bridges_t)
print("False bridges: ", bridges_f)
print("True mountains_or_hills: ", mountains_or_hills_t)
print("False mountains_or_hills: ", mountains_or_hills_f)
print("True statues: ", statues_t)
print("False statues: ", statues_f)
print("True storefront: ", storefront_t)
print("False storefront: ", storefront_f)
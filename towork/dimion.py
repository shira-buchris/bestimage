import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import numpy as np
import model_util
from model_util import DeepModel

import shutil 
from pathlib import Path 

# # from tensorflow.python.keras.applications.mobilenet import MobileNet, preprocess_input
# from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
# from tensorflow.python.keras.preprocessing import image as process_image
# from tensorflow.python.keras.utils import Sequence
# from tensorflow.python.keras.layers import GlobalAveragePooling2D
# from tensorflow.python.keras import Model

model = DeepModel()
image1=r"C:\myproject\PhotosWedding\859A8696.JPG"
image2=r"C:\myproject\PhotosWedding\859A8682.JPG"



# image1 = r"...\5.jpg"
# image2 = r"...\6.jpg"

feat1 = model.preprocess_image(image1)
feat2 = model.preprocess_image(image2)

feat1 = np.expand_dims(feat1, axis=0)
feat2 = np.expand_dims(feat2, axis=0)

feat1 = model._model.predict(feat1)
feat2 = model._model.predict(feat2)

result = DeepModel.cosine_distance(feat1.flatten(), feat2.flatten(), r"C:\myproject\PhotosWedding\859A8696.JPG", r"C:\myproject\PhotosWedding\859A8682.JPG")

print(result)
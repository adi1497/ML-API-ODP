from PIL import Image
from io import BytesIO
import numpy as np
from numpy.lib.type_check import imag
import tensorflow as tf

input_shape = (150, 250, 3)

dict_class_ld = {
    0 : '_DALAM',
    1 : '_LUAR'
}

dict_class_type = {
  0 : 'ODP_CLOSURE',
  1 : 'ODP_PEDESTAL',
  2 : 'ODP_POLE',
  3 : 'ODP_SOLID'
}

dict_class_gb = {
    0 : 'BAD',
    1 : 'GOOD'
}

def read_image(data) -> np.ndarray:
    print(type(data))
    # print(type(BytesIO(data)))
    pil_image = np.array(Image.open(BytesIO(data)))
    return pil_image

def preprocess(image: Image.Image):
    image = np.resize(image, input_shape)
    image = np.asfarray(image)
    #image = image / 127.5 - 1.0
    image = np.expand_dims(image, 0)

    return image

def preprocess_2(image: Image.Image):
    image = np.resize(image, input_shape)
    image = np.asfarray(image)
    image = image / 127.5 - 1.0
    image = np.expand_dims(image, 0)

    return image

def load_model():
  model_ld = tf.keras.models.load_model('image_luar_dalam.h5')

  dict_model_type_by = {
      '_LUAR' : tf.keras.models.load_model('ENB0_v1_ODP_TYPE_LUAR.h5'),
      '_DALAM' : tf.keras.models.load_model('ENB0_v1_ODP_TYPE_DALAM.h5')
  }
  
  dict_model_gb = {
    'ODP_CLOSURE_DALAM':tf.keras.models.load_model('ENB0_v1_ODP_CLOSURE_DALAM.h5'),
    'ODP_CLOSURE_LUAR':tf.keras.models.load_model('ENB0_v1_ODP_CLOSURE_LUAR.h5'),
    'ODP_PEDESTAL_DALAM':tf.keras.models.load_model('ENB0_v1_ODP_PEDESTAL_DALAM.h5'),
    'ODP_PEDESTAL_LUAR':tf.keras.models.load_model('ENB0_v1_ODP_PEDESTAL_LUAR.h5'),
    'ODP_POLE_DALAM':tf.keras.models.load_model('ENB0_v1_ODP_POLE_DALAM.h5'),
    'ODP_POLE_LUAR':tf.keras.models.load_model('ENB0_v1_ODP_POLE_LUAR.h5'),
    'ODP_SOLID_DALAM':tf.keras.models.load_model('ENB0_v1_ODP_SOLID_DALAM.h5'),
    'ODP_SOLID_LUAR':tf.keras.models.load_model('ENB0_v1_ODP_TYPE_LUAR.h5')
  } 

  return model_ld, dict_model_type_by, dict_model_gb

model_ld, dict_model_type, dict_model_gb = load_model()

def predict_by_path(path):
  #im_input = load_gambar_by_path(path)
  im_input = preprocess(path)
  im_input_2 = preprocess_2(path)

  pred_ld = model_ld.predict(im_input_2)
  pred_ld_index = np.argmax(pred_ld, axis=-1)[0]
  pred_ld_class = dict_class_ld[pred_ld_index]

  pred_type = dict_model_type[pred_ld_class].predict(im_input)
  pred_type_index = np.argmax(pred_type, axis=-1)[0]
  pred_type_class = dict_class_type[pred_type_index]

  pred_gb = dict_model_gb[pred_type_class+pred_ld_class].predict(im_input)
  pred_gb_index = np.argmax(pred_gb, axis=-1)[0]
  pred_gb_class = dict_class_gb[pred_gb_index]

  return pred_ld_class,pred_gb_class,pred_type_class
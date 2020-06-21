import tensorflow as tf
import numpy as np
import sys
import cv2
from keras import backend as K
from keras.models import load_model
import warnings
warnings.filterwarnings("ignore")
tf.get_logger().setLevel('ERROR')

K.set_image_data_format('channels_first')
np.set_printoptions(threshold=sys.maxsize)


def img_to_encoding(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Converto l'immagine nel primo canale. Richiesto dal modello pre addestrato di facenet
    img = np.around(np.transpose(img, (2, 0, 1)) / 255.0, decimals=12)

    x_train = np.array([img])

    # Estrazione delle features dal modello addestrato
    embedding = model.predict_on_batch(x_train)
    return embedding


def triplet_loss(y_true, y_pred, alpha=0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

    # Formula triplet loss
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, positive)))
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor, negative)))
    basic_loss = pos_dist - neg_dist + alpha

    loss = tf.maximum(basic_loss, 0.0)

    return loss


# Carico il modello
model = load_model('facenet_model/model.h5', custom_objects={'triplet_loss': triplet_loss})

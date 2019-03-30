# download checkpoint model from http://cs.stanford.edu/people/karpathy/neuraltalk/
import os
import numpy as np
from imagernn.imagernn_utils import decodeGenerator
import pickle
from keras.applications import VGG16,imagenet_utils
from keras.preprocessing.image import load_img,img_to_array
from keras.models import Model
import tensorflow as tf

preprocess = imagenet_utils.preprocess_input

os.environ['CUDA_VISIBLE_DEVICES'] = ''
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
CHECKPOINT_PATH = os.path.join(FILE_DIR, 'models','flickr8k_cnn_lstm_v1.p')

class CaptionGenerator:
    def __init__(self):
        self.checkpoint = pickle.load(open(CHECKPOINT_PATH, 'rb'),encoding='latin1')
        self.checkpoint_params = self.checkpoint['params']
        self.language_model = self.checkpoint['model']
        self.ixtoword = self.checkpoint['ixtoword']
        model = VGG16(weights="imagenet")
        self.visual_model = Model(input=model.input,output=model.layers[21].output)
        self.visual_model._make_predict_function()
        self.graph = tf.get_default_graph()
        self.BEAM_SIZE = 2

    def convert_img_to_vector(self,img_path):
        image = load_img(img_path,target_size=(224,224))
        image = img_to_array(image)
        image = np.expand_dims(image,axis=0)
        image = preprocess(image)
        return image

    def get_image_feature(self,img_path):
        feats = np.transpose(self.visual_model.predict(self.convert_img_to_vector(img_path)))
        return feats

    def predict(self, features):
        BatchGenerator = decodeGenerator(CHECKPOINT_PATH)
        img = {}
        img['feat'] = features[:, 0]
        kwparams = {'beam_size': self.BEAM_SIZE}
        Ys = BatchGenerator.predict([{'image': img}], self.language_model, self.checkpoint_params, **kwparams)
        top_predictions = Ys[0]  # take predictions for the first (and only) image we passed in
        top_prediction = top_predictions[0]  # these are sorted with highest on top
        candidate = ' '.join(
            [self.ixtoword[ix] for ix in top_prediction[1] if ix > 0])  # ix 0 is the END token, skip that
        return candidate

    def get_caption(self, file):
        with self.graph.as_default():
            feat = self.get_image_feature(file)
        caption = self.predict(feat)
        return caption




    

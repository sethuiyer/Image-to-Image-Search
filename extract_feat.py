from keras.applications import VGG16,imagenet_utils
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import Model
preprocess = imagenet_utils.preprocess_input
model = VGG16(weights="imagenet")
new_model = Model(input=model.input,output=model.layers[21].output)

def convert_img_to_vector(img_path):
	image = load_img(img_path,target_size=(224,224))
	image = img_to_array(image)
	image = np.expand_dims(image,axis=0)
	image = preprocess(image)
	return image

def get_image_feature(img_path):
	feats = np.transpose(new_model.predict(convert_img_to_vector(img_path)))
	return feats
	#import scipy.io
	#scipy.io.savemat('vgg_feats.mat',mdict={'feats': np.transpose(feats)})

	

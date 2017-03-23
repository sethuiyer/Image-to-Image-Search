# download checkpoint model from http://cs.stanford.edu/people/karpathy/neuraltalk/
import os.path
import numpy as np
from neuraltalk.imagernn.imagernn_utils import decodeGenerator
import cPickle as pickle
import extract_feat
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
CHECKPOINT_PATH = os.path.join(FILE_DIR, 'model_checkpoint_coco_visionlab43.stanford.edu_lstm_11.14.p')
BEAM_SIZE = 1

class CaptionGenerator:
    def __init__(self):
        self.checkpoint = pickle.load(open(CHECKPOINT_PATH, 'rb'))
        self.checkpoint_params = self.checkpoint['params']
        self.model = self.checkpoint['model']
        self.ixtoword = self.checkpoint['ixtoword']

    def predict(self, features):

        # iterate over all images and predict sentences
        BatchGenerator = decodeGenerator(CHECKPOINT_PATH)
        # encode the image
        img = {}
        img['feat'] = features[:, 0]

        # perform the work. heavy lifting happens inside
        kwparams = {'beam_size': BEAM_SIZE}
        Ys = BatchGenerator.predict([{'image': img}], self.model, self.checkpoint_params, **kwparams)

        # encode the top prediction
        top_predictions = Ys[0]  # take predictions for the first (and only) image we passed in
        top_prediction = top_predictions[0]  # these are sorted with highest on top
        candidate = ' '.join(
            [self.ixtoword[ix] for ix in top_prediction[1] if ix > 0])  # ix 0 is the END token, skip that
        # print 'PRED: (%f) %s' % (top_prediction[0], candidate)

        return candidate

    # absolute file path
    def get_caption(self, file):
	feat = extract_feat.get_image_feature(file)
        caption = self.predict(feat)
        return caption




    

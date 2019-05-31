from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from capgen import CaptionGenerator
import glob
import os

os.environ['CUDA_VISIBLE_DEVICES'] = ''
es = Elasticsearch()
gencap = CaptionGenerator()

def index_database():
    images = glob.glob('static/database/*')
    actions = []
    for i, image in enumerate(images):
        cap = gencap.get_caption(image)
        doc = {'imgurl': image, 'description': cap}
        actions.append(doc)
    bulk(es,actions,index="desearch",doc_type="json")

if __name__ == "__main__":
    index_database()
    print('Images from static/img are indexed successfully')
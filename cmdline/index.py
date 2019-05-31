''' 
Indexes dataset.json in the elastic search server
'''
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

es = Elasticsearch()
with open("dataset.json") as f:
    data = json.load(f)
actions = []
for i in range(len(data['images'])):
        doc = {'id': i, 'imgurl': data['images'][i]['filename'], 'description': data['images'][i]['sentences'][0]['raw'] }
        actions.append(doc)
bulk(es,actions,index="desearch",doc_type="json")
es.indices.refresh(index="desearch")

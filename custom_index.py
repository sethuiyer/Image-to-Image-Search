''' 
Indexes custom_dataset.json in the elastic search server.

The format of the custom dataset file should be like this:
{'images':[
    {'imgurl': path_to_image1, 
    'description': Description of the image1
    },
    {'imgurl': path_to_image2, 
    'description': Description of the image2
    },
    ...
    {'imgurl': path_to_image_n, 
    'description': Description of the image_n
    }
        ]
}
'''
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

es = Elasticsearch()
with open("custom_dataset.json") as f:
    data = json.load(f)
actions = []
for i in range(len(data['images'])):
        doc = {'id': i, 'imgurl': data['images'][i]['imgurl'], 'description': data['images'][i]['description'] }
        actions.append(doc)
bulk(es,actions,index="desearch",doc_type="json")
es.indices.refresh(index="desearch")

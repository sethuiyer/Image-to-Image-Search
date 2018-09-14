import os
import numpy as np
from PIL import Image
from capgen import CaptionGenerator
from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json

os.environ['CUDA_VISIBLE_DEVICES'] = ''
es = Elasticsearch()
gencap = CaptionGenerator()

def index_data():
    global es
    with open("dataset.json") as f:
        data = json.load(f)
    actions = []
    for i in range(len(data['images'])):
        doc = {'id': i, 'imgurl': data['images'][i]['filename'], 'description': data['images'][i]['sentences'][0]['raw'] }
        actions.append(doc)
    bulk(es,actions,index="desearch",doc_type="json")

def description_search(query):
    global es
    results = es.search(
        index="desearch",
        body={
            "size": 4,
            "query": {
            "match": {"description": query}
            }
            })
    hitCount = results['hits']['total']
    if hitCount > 0:
        if hitCount is 1:
            print(str(hitCount),' result')
        else:
            print(str(hitCount), 'results')
        answers =[]  
        for hit in results['hits']['hits']:
            desc = hit['_source']['description']
            imgurl = 'static/img/'+ hit['_source']['imgurl']
            answers.append([imgurl,desc])
    else:
        answers = []
    return answers


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    global gencap
    if request.method == 'POST':
        file = request.files['query_img']

        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/" + file.filename
        img.save(uploaded_img_path)
        query = gencap.get_caption(uploaded_img_path)
        answers = description_search(query)

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               answers=answers)
    else:
        return render_template('index.html')

if __name__=="__main__":
    try:
        index_data()
    except Exception as e:
        pass
    app.run("127.0.0.1", debug=False)

import glob
import os

from PIL import Image
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename
import json

from capgen import CaptionGenerator

os.environ['CUDA_VISIBLE_DEVICES'] = ''
es = Elasticsearch()
gencap = CaptionGenerator()


def description_search(query):
    global es
    results = es.search(
        index="desearch",
        body={
            "size": 20,
            "query": {
                "match": {"description": query}
            }
        })
    hitCount = results['hits']['total']['value']
    print(results)

    if hitCount > 0:
        if hitCount is 1:
            print(str(hitCount), ' result')
        else:
            print(str(hitCount), 'results')
        answers = []
        max_score = results['hits']['max_score']

        if max_score >= 0.35:
            for hit in results['hits']['hits']:
                if hit['_score'] > 0.5 * max_score:
                    desc = hit['_source']['description']
                    imgurl = hit['_source']['imgurl']
                    answers.append([imgurl, desc])
    else:
        answers = []
    return answers


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'database')
app.config['TEMP_UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    global gencap
    if request.method == 'POST':
        if 'query_img' not in request.files or request.files['query_img'].filename == '' or not allowed_file(
                request.files['query_img'].filename):
            return render_template('search.html')
        file = request.files['query_img']
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], file.filename)
        img.save(uploaded_img_path)
        query = gencap.get_caption(uploaded_img_path)
        answers = description_search(query)

        return render_template('search.html',
                               query_path=uploaded_img_path,
                               answers=answers)
    else:
        return render_template('search.html')


@app.route('/api/search', methods=['POST'])
def api_search():
    global gencap
    if 'query_img' not in request.files or request.files['query_img'].filename == '' or not allowed_file(
            request.files['query_img'].filename):
        return Response(response=json.dumps({'success': False, 'message': 'Uploaded image is invalid or not allowed'}),
                        status=400, mimetype="application/json")
    file = request.files['query_img']
    img = Image.open(file.stream)  # PIL image
    uploaded_img_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], file.filename)
    img.save(uploaded_img_path)
    query = gencap.get_caption(uploaded_img_path)
    answers = description_search(query)

    return Response(response=json.dumps({'success': True, 'answers': answers}),
                    status=200, mimetype="application/json")


@app.route('/database')
def database():
    images = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*'))
    return render_template('database.html', database_images=images)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'photos' not in request.files:
            return render_template('database.html')
        actions = []
        for file in request.files.getlist('photos'):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                cap = gencap.get_caption(file_path)
                doc = {'imgurl': file_path, 'description': cap}
                actions.append(doc)
        bulk(es, actions, index="desearch", doc_type="json")
        return render_template('database.html')


@app.route('/caption', methods=['GET', 'POST'])
def caption():
    if request.method == 'POST':
        if 'query_img' not in request.files or request.files['query_img'].filename == '' or not allowed_file(
                request.files['query_img'].filename):
            return render_template('caption.html')
        file = request.files['query_img']
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], file.filename)
        img.save(uploaded_img_path)
        cap = gencap.get_caption(uploaded_img_path)
        return render_template('caption.html', caption=cap, query_path=uploaded_img_path)
    else:
        return render_template('caption.html')


@app.route('/api/caption', methods=['POST'])
def caption_api():
    if 'query_img' not in request.files or request.files['query_img'].filename == '' or not allowed_file(
            request.files['query_img'].filename):
        return Response(response=json.dumps({'success': False, 'message': 'Uploaded image is invalid or not allowed'}),
                        status=400, mimetype="application/json")
    file = request.files['query_img']
    img = Image.open(file.stream)  # PIL image
    uploaded_img_path = os.path.join(app.config['TEMP_UPLOAD_FOLDER'], file.filename)
    img.save(uploaded_img_path)
    cap = gencap.get_caption(uploaded_img_path)
    return Response(response=json.dumps({'success': True, 'caption': cap}),
                    status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run("127.0.0.1", debug=True)

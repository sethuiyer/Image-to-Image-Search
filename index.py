''' 
Indexes dataset.json in the elastic search server
'''
import elasticsearch
import json
es = elasticsearch.Elasticsearch()  

print 'Indexing the data to the Elastic Search Server.. Would take some time'
with open("dataset.json") as f:
    data = json.load(f)
num_rec = len(data['images'])
new_d = [ {} for _ in xrange(num_rec)]

for _ in xrange(num_rec):
    new_d[_]['imgurl'] = data['images'][_]['filename']
    new_d[_]['description'] = data['images'][_]['sentences'][0]['raw']
for i in xrange(num_rec):
    es.index(index="desearch", doc_type="json", id=i, body = {
                    'imgurl': new_d[i]['imgurl'],
                    'description': new_d[i]['description'],
                    'idnum': i
                })
print 'Done!'
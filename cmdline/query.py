from elasticsearch import Elasticsearch
es = Elasticsearch() 

def description_search(query):
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
            imgurl = hit['_source']['imgurl']
            answers.append({'URL':imgurl,'Description':desc})
    else:
        answers = []
    return answers


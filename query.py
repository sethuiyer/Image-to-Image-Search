import elasticsearch
es = elasticsearch.Elasticsearch()  # use default of localhost, port 9200

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
            print str(hitCount),' result'
        else:
            print str(hitCount), 'results' 
        answers =[]  
        for hit in results['hits']['hits']:
            desc = hit['_source']['description']
            imgurl = hit['_source']['imgurl']
            idnum = hit['_source']['idnum']
            score = hit['_score']
            fetch_result = es.get(index="desearch", doc_type="json", id=idnum)
            answers.append({'URL':fetch_result['_source']['imgurl'],'Description':fetch_result['_source']['description']})
    else:
        answers = []
    return answers


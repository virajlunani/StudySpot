from whoosh.fields import *
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser

import json

def index_documents():
    schema = Schema(title=TEXT(stored=True), content=TEXT)
    ix = create_in("search_index", schema)
    writer = ix.writer()
    with open('places.json') as f:
        places = json.load(f)
        for place in places:
            title = place['name']
            content = place['description'] + ' ' + place['noise'] + ' ' + place['location'] + ' ' + place['address']
            writer.add_document(title=title, content=content)
    writer.commit()

def search_index(q):
    results = []
    ix = open_dir('search_index')
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(q)
        res = searcher.search(query)
        for r in res:
            with open('places.json') as f:
                places = json.load(f)
                for place in places:
                    if place['name'] == r['title']:
                        results.append(place)
    return results

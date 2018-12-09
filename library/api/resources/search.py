from elasticsearch.helpers import bulk
from flask_restful import request, Resource
from flask import current_app

from library.utils.search import indexGen

# Global Search Resource
class Search(Resource):
    def get(self):
        es = current_app.es
        search_string = request.args.get("q")
        if not search_string:
            return {"error": "q query parameter is mandatory for search"}, 404

        search_body = {
            "query": {
                "multi_match": {
                    "query": search_string,
                    "fields": ["book.title", "book.author.first_name"],
                    "fuzziness": "AUTO"
                }
            }
        }
        return es.search(index='library_book', doc_type='_doc', body=search_body)["hits"]

    def post(self):
        # reindex, admin functionality
        result =bulk(es, indexGen('library_book', '_doc'))
        # result = es.index(index='library_book', doc_type='_doc', id="1", body={"test": "test"})

        return result

    def delete(self):
        # remove index, admin functionality
        es.indices.delete(index='library')
        return {}
import os
from elasticsearch import Elasticsearch

es_url = os.environ.get('ELASTICSEARCH_URL', 'http://es:9200')
es = Elasticsearch(es_url)


INDEX_NAME = "notes"

def create_index_if_not_exists():
    if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME, body={
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "body": {"type": "text"},
                        "tags": {"type": "keyword"},
                        "created_at": {"type": "date"}
                    }
                }
            })
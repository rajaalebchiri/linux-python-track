from elasticsearch import Elasticsearch

es = Elasticsearch("http://0.0.0.0:9200")

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

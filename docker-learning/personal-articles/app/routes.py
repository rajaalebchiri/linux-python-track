from flask import Blueprint, request, jsonify
from datetime import datetime
from .es_client import es, INDEX_NAME, create_index_if_not_exists

articles_bp = Blueprint('articles', __name__)
create_index_if_not_exists()

@articles_bp.route('/articles', methods=['POST'])
def add_note():
    data = request.get_json()
    note = {
        "title": data.get("title"),
        "body": data.get("body"),
        "tags": data.get("tags", []),
        "created_at": datetime.utcnow()
    }
    res = es.index(index=INDEX_NAME, document=note)
    return jsonify({"result": "Note added", "id": res['_id']}), 201

@articles_bp.route('/articles', methods=['GET'])
def list_articles():
    res = es.search(index=INDEX_NAME, query={"match_all": {}}, size=10)
    articles = [doc['_source'] for doc in res['hits']['hits']]
    return jsonify(articles)

@articles_bp.route('/search', methods=['GET'])
def search_articles():
    query = request.args.get("q", "")
    tag = request.args.get("tag")

    es_query = {
        "bool": {
            "must": [{"multi_match": {"query": query, "fields": ["title", "body"]}}] if query else [],
            "filter": [{"terms": {"tags": [tag]}}] if tag else []
        }
    }

    res = es.search(index=INDEX_NAME, query=es_query, size=10)
    articles = [doc['_source'] for doc in res['hits']['hits']]
    return jsonify(articles)

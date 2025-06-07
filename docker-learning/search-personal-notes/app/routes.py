from flask import Blueprint, request, jsonify
from datetime import datetime
from .es_client import es, INDEX_NAME, create_index_if_not_exists

notes_bp = Blueprint('notes', __name__)
create_index_if_not_exists()

@notes_bp.route('/notes', methods=['POST'])
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

@notes_bp.route('/notes', methods=['GET'])
def list_notes():
    res = es.search(index=INDEX_NAME, query={"match_all": {}}, size=10)
    notes = [doc['_source'] for doc in res['hits']['hits']]
    return jsonify(notes)

@notes_bp.route('/search', methods=['GET'])
def search_notes():
    query = request.args.get("q", "")
    tag = request.args.get("tag")

    es_query = {
        "bool": {
            "must": [{"multi_match": {"query": query, "fields": ["title", "body"]}}] if query else [],
            "filter": [{"terms": {"tags": [tag]}}] if tag else []
        }
    }

    res = es.search(index=INDEX_NAME, query=es_query, size=10)
    notes = [doc['_source'] for doc in res['hits']['hits']]
    return jsonify(notes)

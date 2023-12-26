from flask import request, Blueprint

vector_db_api = Blueprint('vector_db_api', __name__)

from chroma import VectorDB
from utils.vector_db import format_messages
from utils.api import wrap_response

# vector database - chromadb
vector_db = VectorDB()

@vector_db_api.route("/vectordb/init", methods=['POST'])
def init_database():
    phone = request.json['phone']
    try:
        vector_db.init(phone)
        return wrap_response()
    except ValueError:
        return wrap_response('user has existed', 400)


@vector_db_api.route("/vectordb/messages", methods=['POST'])
def add_messages():
    body = request.json

    try:
        phone = body['phone']
        contents, roles = format_messages(body['messages'])
    except KeyError as e:
        return wrap_response(repr(e), 400)

    try:
        vector_db.append_messages(phone, contents, roles)
        return wrap_response()
    except FileNotFoundError:
        return wrap_response('user not found', 404)
    except ValueError as e:
        return wrap_response(repr(e), 400)


@vector_db_api.route("/vectordb/messages", methods=['GET'])
def clear_messages():
    phone = request.args.get('phone')
    result = vector_db.get_messages(phone)
    return wrap_response({
        "messages": result['documents']
    })  

@vector_db_api.route("/vectordb/messages/all", methods=['DELETE'])
def get_messages():
    try:
        phone = request.json['phone']
        vector_db.clear_messages(phone)
        return wrap_response()
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_response(repr(e), 404)
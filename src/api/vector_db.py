from flask import request, Blueprint

vector_db_api = Blueprint('vector_db_api', __name__)

from chroma import VectorDB
from utils.vector_db import format_messages
from utils.api import wrap_response, wrap_error, recv_info, recv_info_from_param

# vector database - chromadb
vector_db = VectorDB()

@vector_db_api.route("/vectordb/init", methods=['POST'])
def init_database():
    try:
        info = recv_info()
        vector_db.init(info)
        return wrap_response()
    except (KeyError, ValueError) as e:
        return wrap_error(e, 400)

@vector_db_api.route("/vectordb/messages", methods=['POST'])
def add_messages():
    try:
        info = recv_info()
        contents, roles = format_messages(request.json['messages'])
        vector_db.append_messages(info, contents, roles)
        return wrap_response()
    except (KeyError, ValueError) as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_error(e, 404)

@vector_db_api.route("/vectordb/messages", methods=['GET'])
def get_messages():
    try:
        # Notice: Get Request here
        info = recv_info_from_param()
        
        # whether it will return with id
        try:
            need_id = int(request.args.get('needId')) == 1
        except ValueError:
            need_id = False

        messages = vector_db.get_messages(info, need_id)
        return wrap_response({
            "messages": messages
        })  
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_error(e, 404)

@vector_db_api.route("/vectordb/messages/all", methods=['DELETE'])
def clear_messages():
    try:
        info = recv_info()
        vector_db.clear_messages(info)
        return wrap_response()
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_error(e, 404)
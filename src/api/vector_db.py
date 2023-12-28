from flask import request, Blueprint

vector_db_api = Blueprint('vector_db_api', __name__)

from chroma import VectorDB
from utils.vector_db import format_messages
from utils.api import wrap_response, wrap_error

# vector database - chromadb
vector_db = VectorDB()

def recv_info():
    try:
        phone = request.json['phone']
        bot_role = request.json['botRole']
    except:
        raise KeyError("key info not found")

    return {
        "phone": phone, 
        "botRole": bot_role
    }

def recv_info_from_param():
    try:
        return {
            "phone": request.args.get('phone'),
            "botRole": request.args.get('botRole')
        }
    except:
        raise KeyError("key info not found")

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
    except KeyError as e:
        return wrap_response(repr(e), 400)

    try:
        vector_db.append_messages(info, contents, roles)
        return wrap_response()
    except FileNotFoundError:
        return wrap_response('user not found', 404)
    except ValueError as e:
        return wrap_response(repr(e), 400)


@vector_db_api.route("/vectordb/messages", methods=['GET'])
def get_messages():
    try:
        # Notice: Get Request here
        info = recv_info_from_param()
        messages = vector_db.get_messages(info)
        return wrap_response({
            "messages": messages
        })  
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError:
        return wrap_response("User or BotRole not found", 404)

@vector_db_api.route("/vectordb/messages/all", methods=['DELETE'])
def clear_messages():
    try:
        info = recv_info()
        vector_db.clear_messages(info)
        return wrap_response()
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_response(repr(e), 404)
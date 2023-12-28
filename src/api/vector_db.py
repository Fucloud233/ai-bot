from flask import request, Blueprint

vector_db_api = Blueprint('vector_db_api', __name__)

from chroma import VectorDB
from utils.vector_db import format_messages
from utils.api import wrap_response, wrap_error

# vector database - chromadb
vector_db = VectorDB()

def get_basic_info():
    try:
        phone = request.json['phone']
        bot_role = request.json['botRole']
    except:
        raise KeyError("key info not found")

    return phone, bot_role

@vector_db_api.route("/vectordb/init", methods=['POST'])
def init_database():
    try:
        phone, bot_role = get_basic_info()
        vector_db.init(phone, bot_role)
        return wrap_response()
    except (KeyError, ValueError) as e:
        return wrap_error(e, 400)

@vector_db_api.route("/vectordb/messages", methods=['POST'])
def add_messages():
    try:
        phone, bot_role = get_basic_info()
        contents, roles = format_messages(request.json['messages'])
    except KeyError as e:
        return wrap_response(repr(e), 400)

    try:
        vector_db.append_messages(phone, bot_role, contents, roles)
        return wrap_response()
    except FileNotFoundError:
        return wrap_response('user not found', 404)
    except ValueError as e:
        return wrap_response(repr(e), 400)


@vector_db_api.route("/vectordb/messages", methods=['GET'])
def get_messages():
    try:
        # Notice: Get Request here
        phone = request.args.get('phone')
        bot_role = request.args.get('botRole')
        messages = vector_db.get_messages(phone, bot_role)
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
        phone, bot_role = get_basic_info()
        vector_db.clear_messages(phone, bot_role)
        return wrap_response()
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_response(repr(e), 404)
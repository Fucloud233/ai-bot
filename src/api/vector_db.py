from flask import request, Blueprint

vector_db_api = Blueprint('vector_db_api', __name__)

from chroma import VectorDB
from utils.vector_db import format_messages
from utils.api import wrap_response, wrap_error
import utils.api as apiUtils

# vector database - chromadb
vector_db = VectorDB()

@vector_db_api.route("/vectordb/init", methods=['POST'])
def init_database():
    try:
        info = apiUtils.body_index()
        vector_db.init(info)
        return wrap_response()
    except (KeyError, ValueError) as e:
        return wrap_error(e, 400)

@vector_db_api.route("/vectordb/messages", methods=['POST'])
def add_messages():
    try:
        info = apiUtils.body_index()
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
        info = apiUtils.param_index()
        
        # whether it will return with id
        need_id = apiUtils.param_bool('needId')
        need_time = apiUtils.param_bool('needTime')

        messages = vector_db.get_messages(info, need_id, need_time)
        return wrap_response({
            "messages": messages
        })  
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_error(e, 404)

@vector_db_api.route("/vectordb/messages/nearest", methods=['GET'])
def get_nearest_messages():
    try:
        messages = vector_db.get_nearest_messages(
            apiUtils.param_index(),
            apiUtils.param_int("number", 10),
            apiUtils.param_int("offset", 0),
            apiUtils.param_int("n", 10),
            apiUtils.param_bool("needId"),
            apiUtils.param_bool("needTime")
        )
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
        info = apiUtils.body_info()
        vector_db.clear_messages(info)
        return wrap_response()
    except KeyError as e:
        return wrap_response(repr(e), 400)
    except FileNotFoundError as e:
        return wrap_error(e, 404)
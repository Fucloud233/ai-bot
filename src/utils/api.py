from flask import make_response, request
    
from utils.vector_db import DBIndex, PHONE, BOT_ROLE

def body_index() -> DBIndex:
    try:
        body = request.json
        return DBIndex(body[PHONE], body[BOT_ROLE])
    except:
        raise KeyError("key info not found")

def param_index() -> DBIndex:
    try:
        args = request.args
        return DBIndex(args[PHONE], args[BOT_ROLE])
    except:
        raise KeyError("key info not found")
    
def param_bool(name, default: bool=False):
    value = default
    try:
        value = int(request.args.get(name)) == 1
    except:
        pass
    
    return value

def param_int(name, default: bool=0):
    value = default
    try:
        value = int(request.args.get(name))
    except:
        pass

    return value

def wrap_response(msg: str='', status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

def wrap_answer(answer: str):
    return make_response({
        "message": answer
    }, 200)

def wrap_error(err: Exception, status_code: int):
    if len(err.args) > 0:
        message = err.args[0]
    else:
        message = repr(err)
        status_code = 500

    resp = make_response({
        "message": message
    })
    resp.status_code = status_code
    return resp

def check_messages(messages):
    if type(messages) != list:
        raise TypeError("The format of messages is incorrect!")

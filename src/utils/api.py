from flask import make_response

def wrap_response(msg: str='', status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

def wrap_error(err: Exception, status_code: int):
    resp = make_response(err.args[0])
    resp.status_code = status_code
    return resp

def check_messages(messages):
    if type(messages) != list:
        raise TypeError("The format of messages is incorrect!")

from flask import make_response

def wrap_response(msg: str='', status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

def check_messages(messages):
    if type(messages) != list:
        raise TypeError("The format of messages is incorrect!")

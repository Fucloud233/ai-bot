from flask import make_response, request
    
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

def wrap_response(msg: str='', status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

def wrap_error(err: Exception, status_code: int):
    resp = make_response({
        "message": err.args[0]
    })
    resp.status_code = status_code
    return resp

def check_messages(messages):
    if type(messages) != list:
        raise TypeError("The format of messages is incorrect!")

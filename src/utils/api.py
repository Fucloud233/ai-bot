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
    
def recv_bool_from_parm(name, default: bool=False):
    value = default
    try:
        value = int(request.args.get(name)) == 1
    except:
        pass
    
    return value

def wrap_response(msg: str='', status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

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

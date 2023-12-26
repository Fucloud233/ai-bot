from flask import request
from utils.api import wrap_response

from api import app
from bot import Bot, BotRole

bot = Bot()

# post request
@app.route("/chat", methods=['POST'])
def chat():
    messages = request.json['messages']

    try:
        # check whether the messages is list
        if type(messages) != list:
            raise TypeError("The format of messages is incorrect!")
        result = bot.talk(messages)
    except BaseException as e:
        return wrap_response(repr(e), 400)

    return wrap_response(result)

@app.route("/chat/<string:role_name>", methods=['POST'])
def chat_with_role(role_name):
    try:
        # get the role
        role = BotRole.new(role_name)

        # get and check message
        messages = request.json['messages']
        wrap_response(messages)

        # generate and return result
        result = bot.talk_with_role(messages, role)
        return wrap_response(result)
    except ValueError as e:
        return wrap_response(f"Role '{role_name}' not found", 404)
    except TypeError as e:
        print(e.with_traceback())
        return wrap_response(repr(e), 400)
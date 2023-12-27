from flask import request, Blueprint
from typing import List

bot_api = Blueprint('bot_api', __name__)

from utils.api import wrap_response
from utils.prompt import wrap_prompt
from bot import Bot, BotRole, User, Assistant

bot = Bot()

# post request
@bot_api.route("/chat", methods=['POST'])
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

@bot_api.route('/chat/<string:role_name>', methods=['POST'])
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
    

from api.vector_db import vector_db

@bot_api.route("/chat/enhance", methods=['POST'])
def chat_with_role_enhance():
    body = request.json

    # 1. catch the message
    try:
        phone = body['phone']
        bot_role = BotRole.new(body["botRole"])
        user_message = body['userMessage']

        # optional
        bot_role_description = body.get("BotRoleDescription")
        history_messages: List = body.get("historyMessages")

        if bot_role_description is None:
            bot_role_description = ""
        if history_messages is None:
            history_messages = []
        
    except KeyError as e:
        return wrap_response(repr(e), 400)
    
    # 2. merge the basic prompt and role
    try:
        vector_db.query("18212345678", "你好")

        history_messages.append(wrap_prompt(user_message))

        result = bot.talk_with_custom_role(
            history_messages,
            bot_role,
            bot_role_description
        )

        vector_db.append_messages(phone, [user_message, result], [User, Assistant])

        return wrap_response(result)
    except Exception as e:
        return wrap_response(repr(e), 400)
    

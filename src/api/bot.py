from flask import request, Blueprint
from typing import List
from pprint import pprint

bot_api = Blueprint('bot_api', __name__)

from utils.api import wrap_response, wrap_error, recv_info
from utils.prompt import wrap_user_prompt, BotRole, User, Assistant
from bot.ernie import ErineBot

bot = ErineBot()

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
    except FileNotFoundError as e:
        return wrap_error(e, 400)
    except (ValueError, TypeError) as e:
        return wrap_error(e, 400)
    

from api.vector_db import vector_db

@bot_api.route("/chat/enhance", methods=['POST'])
def chat_with_role_enhance():
    body = request.json

    try:
        # 1. catch the message
        info = recv_info()
        user_message = body['userMessage']

        # optional
        bot_role_description = body.get("BotRoleDescription")
        history_messages: List = body.get("historyMessages")

        if bot_role_description is None:
            bot_role_description = ""
        if history_messages is None:
            history_messages = []
        
        # 2. merge the basic prompt and role
        messages = []

        # (1) similar context
        context_messages = vector_db.query_with_context(info, user_message)
        messages.extend(context_messages)
        # print("context: "); pprint(context_messages)

        # (2) history messages
        messages.extend(history_messages)

        # (3) user message
        messages.append(wrap_user_prompt(user_message))

        # 3. talk with bot
        result = bot.talk_with_custom_role(
            messages,
            BotRole.new(info['botRole']),
            bot_role_description
        )

        # vector_db.append_messages(phone, [user_message, result], [User, Assistant])

        return wrap_response(result)
    except (KeyError, ValueError) as e:
        return wrap_error(e, 400)
    

from flask import request, Blueprint
from typing import List
from pprint import pprint
from datetime import datetime

bot_api = Blueprint('bot_api', __name__)

from utils.api import wrap_response, wrap_error
from utils.prompt import wrap_user_prompt, BotRole, User, Assistant
from utils.config import Config, BotKind
import utils.api as apiUtils

def get_bot():
    match Config.BotKind:
        case BotKind.Erine:
            from bots.ernie import ErineBot
            return ErineBot()
        case BotKind.GPT:
            from bots.gpt import GPTBot
            return GPTBot()

bot = get_bot()

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

def merge_messages(index, user_message):
    messages = []

    # (1) similar context
    similar = vector_db.query_similar_context(index, user_message)

    # (2) history messages
    history = vector_db.get_nearest_messages(index, n=2)

    print("similar: ", similar.begin, similar.end)
    print("history: ", history.begin, history.end)

    # (3) merge similar and history messages
    summarized = ""
    if similar.end >= history.begin:
        history_messages = history.messages[similar.end:]
        messages.extend(similar.messages)
        messages.extend(history_messages)
    elif similar.begin < similar.end:
        messages.extend(history.messages)
        summarized = bot.summarize_history_messages(similar.messages)
        
    # (4) user message
    messages.append(wrap_user_prompt(user_message))
    
    return messages, summarized

@bot_api.route("/chat/enhance", methods=['POST'])
def chat_with_role_enhance():
    body = request.json

    try:
        # record user's message time (query)
        query_time = datetime.now()

        # 1. catch the message
        index = apiUtils.body_index()
        user_message = body['userMessage']

        # optional
        bot_role_description = body.get("BotRoleDescription")

        if bot_role_description is None:
            bot_role_description = ""
        
        # 2. merge the basic prompt and role
        messages, summarized = merge_messages(index, user_message)

        # 3. talk with bot
        result = bot.talk_with_custom_role(
            messages,
            BotRole.new(index.bot_role),
            bot_role_description,
            summarized
        )

        # record bot's message time (answer)
        answer_time = datetime.now()

        vector_db.append_messages(index, [user_message, result], [User, Assistant], [query_time, answer_time])

        return apiUtils.wrap_answer(result)
    except (KeyError, ValueError) as e:
        return wrap_error(e, 400)
    

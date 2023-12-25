from flask import Flask, request, send_file, make_response
# https://segmentfault.com/a/1190000024515972
from flask_cors import CORS

from bot import Bot, BotRole
from chroma import VectorDB
from typing import List

from utils.vector_db import format_messages

# flask
app = Flask("ai-bot")
CORS(app, supports_credentials=True)
# bot
bot = Bot()
# vector database - chromadb
vector_db = VectorDB()

def gen_return_msg(msg: str='', status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

def check_messages(messages):
    if type(messages) != list:
        raise TypeError("The format of messages is incorrect!")

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
        return gen_return_msg(repr(e), 400)

    return gen_return_msg(result)

@app.route("/chat/<string:role_name>", methods=['POST'])
def chat_with_role(role_name):
    try:
        # get the role
        role = BotRole.new(role_name)

        # get and check message
        messages = request.json['messages']
        check_messages(messages)

        # generate and return result
        result = bot.talk_with_role(messages, role)
        return gen_return_msg(result)
    except ValueError as e:
        return gen_return_msg(f"Role '{role_name}' not found", 404)
    except TypeError as e:
        print(e.with_traceback())
        return gen_return_msg(repr(e), 400)
    

@app.route("/vectordb/init", methods=['POST'])
def init_database():
    phone = request.json['phone']
    try:
        vector_db.init(phone)
        return gen_return_msg()
    except ValueError:
        return gen_return_msg('user has existed', 400)


@app.route("/vectordb/messages", methods=['POST'])
def add_messages():
    body = request.json

    try:
        phone = body['phone']
        contents, roles = format_messages(body['messages'])
    except KeyError as e:
        return gen_return_msg(repr(e), 400)

    try:
        vector_db.append_messages(phone, contents, roles)
        return gen_return_msg()
    except FileNotFoundError:
        return gen_return_msg('user not found', 404)
    except ValueError as e:
        return gen_return_msg(repr(e), 400)


@app.route("/vectordb/messages", methods=['GET'])
def clear_messages():
    phone = request.args.get('phone')
    result = vector_db.get_messages(phone)
    return gen_return_msg({
        "messages": result['documents']
    })  

@app.route("/vectordb/messages/all", methods=['DELETE'])
def get_messages():
    try:
        phone = request.json['phone']
        vector_db.clear_messages(phone)
        return gen_return_msg()
    except KeyError as e:
        return gen_return_msg(repr(e), 400)
    except FileNotFoundError as e:
        return gen_return_msg(repr(e), 404)
    

# @app.route("/chroma/messages/similar")
# def 

# @app.route("/chroma/messages/newest")
# def 
    


if __name__ == '__main__':
    app.run(port=6061, host="0.0.0.0", debug=True)
from flask import Flask, request, send_file, make_response
# https://segmentfault.com/a/1190000024515972
from flask_cors import CORS

from bot import Bot
from typing import List



app = Flask("ai-bot")
CORS(app, supports_credentials=True)

bot = Bot()

def gen_return_msg(msg: str, status_code: int=200):
    response = make_response(msg)
    response.status_code = status_code
    return response

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
         
if __name__ == '__main__':
    app.run(port=8081, host="0.0.0.0", debug=False)
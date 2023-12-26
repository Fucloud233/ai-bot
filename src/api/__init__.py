from flask import Flask
# https://segmentfault.com/a/1190000024515972
from flask_cors import CORS

from api.bot import bot_api
from api.vector_db import vector_db_api

# flask
app = Flask("ai-bot")
CORS(app, supports_credentials=True)

app.register_blueprint(bot_api)
app.register_blueprint(vector_db_api)
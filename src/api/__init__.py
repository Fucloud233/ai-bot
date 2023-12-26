from flask import Flask, request, send_file, make_response
# https://segmentfault.com/a/1190000024515972
from flask_cors import CORS

# flask
app = Flask("ai-bot")
CORS(app, supports_credentials=True)
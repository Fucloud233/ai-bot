import erniebot
from config import Config


# set api key
erniebot.api_type = Config.api_type
erniebot.access_token = Config.access_token

models = erniebot.Model.list()

print(models)
print(Config.access_token)
print(Config.api_type)
import erniebot
from config import Config
from enum import Enum

# https://github.com/PaddlePaddle/ERNIE-Bot-SDK

# set api key
erniebot.api_type = Config.api_type
erniebot.access_token = Config.access_token

models = erniebot.Model.list()

class ModelKind(Enum):
    Ernie = 'ernie-bot'
    ErnieTurbo = 'ernie-bot-turbo'
    Ernie4 = 'ernie-bot-4'

class Bot:
    @staticmethod
    def talk(messages, model_kind: ModelKind=ModelKind.Ernie):
        response = erniebot.ChatCompletion.create(
            model=model_kind.value,
            messages=messages
        )

        return response['result']
    
def main():
    print(Bot.talk([{
        "role": "user",
        "content": "请问你是谁？",
    }]))

if __name__ == '__main__':
    main()
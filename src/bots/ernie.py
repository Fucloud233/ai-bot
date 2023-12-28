import erniebot
from enum import Enum
from typing import List

from bots.base import BasicBot
from utils.config import ErineConfig

# https://github.com/PaddlePaddle/ERNIE-Bot-SDK

# set api key
erniebot.api_type = ErineConfig.ApiType
erniebot.access_token = ErineConfig.AccessToken

models = erniebot.Model.list()

class ModelKind(Enum):
    Ernie = 'ernie-bot'
    ErnieTurbo = 'ernie-bot-turbo'
    Ernie4 = 'ernie-bot-4'

class ErineBot(BasicBot):
    model_kind = ModelKind=ModelKind.Ernie

    def __init__(self):
        pass

    def _call_api(self, messages: List[str]):
        print("hello")

        try:
            response = erniebot.ChatCompletion.create(
                model=ErineBot.model_kind.value,
                messages=messages
            )
            
        except erniebot.errors.InvalidArgumentError as e:
            raise ValueError(e.args[0])
        except erniebot.errors.InvalidTokenError as e:
            raise PermissionError(e.args[0])
        
        return response['result']

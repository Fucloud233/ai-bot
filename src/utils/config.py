import json
from enum import Enum

class ErineConfig:
    ApiType = None
    AccessToken = None

    @staticmethod
    def from_file(info):
        if info is None:
            return

        ErineConfig.ApiType = info.get("apiType")
        ErineConfig.AccessToken = info.get("accessToken")


class GPTConfig:
    ApiKey = None

    @staticmethod
    def from_file(info):
        if info is None:
            return
        
        GPTConfig.ApiKey = info.get("apiKey")

        if GPTConfig.ApiKey == None:
            print("GPT api key is None")
            exit(1)


class BotKind(Enum):
    Erine = 'ernie'
    GPT = 'gpt'

    def new(kind):
        return BotKind(kind)
    
    @property
    def config(self):
        match self:
            case BotKind.Erine: return ErineConfig
            case BotKind.GPT: return GPTConfig
        
        return None
        

class Config:
    BotKind = None
    # chroma
    DatabasePath = 'data/chroma'

    @staticmethod
    def init():
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)

                # bot_kind
                bot_kind = BotKind.new(config['botKind'])
                bot_kind.config.from_file(config['key'].get(bot_kind.value))
                Config.BotKind = bot_kind

                database_path = config.get('databasePath')
                if database_path != None and database_path != "":
                    Config.DatabasePath = database_path
        except Exception as e:
            print(repr(e))
            exit(1)

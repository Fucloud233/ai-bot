import json

class ErineConfig:
    ApiType = None
    AccessToken = None

    @staticmethod
    def from_file(info):
        if info is None:
            return

        ErineConfig.ApiType = info.get("apiType")
        ErineConfig.AccessToken = info.get("accessToken")


class ChatGPTConfig:
    ApiKey = None

    @staticmethod
    def from_file(info):
        if info is None:
            return
        
        ChatGPTConfig.ApiKey = info.get("apiKey")
        

class Config:
    LlmKind = None
    # chroma
    DatabasePath = 'data/chroma'

    Erine =  ErineConfig
    ChatGPT = ChatGPTConfig

    @staticmethod
    def init():
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                Config.LlmKind = config['llmKind']

                database_path = config.get('databasePath')
                if database_path != None and database_path != "":
                    Config.DatabasePath = database_path

                ErineConfig.from_file(config['key'].get('erine'))
                ChatGPTConfig.from_file(config['key'].get('chatGPT'))

        except Exception as e:
            print(repr(e))
            exit(1)

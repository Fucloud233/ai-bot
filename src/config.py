import json

class Config:
    api_type = ""
    access_token = ""

    # chroma
    database_path = 'data/chroma'

    @staticmethod
    def init():
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                Config.api_type = config['api_type']
                Config.access_token = config['access_token']
        except Exception as e:
            print(repr(e))
            exit(1)


Config.init()
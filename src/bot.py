import erniebot
from config import Config
from enum import Enum
from typing import List

# https://github.com/PaddlePaddle/ERNIE-Bot-SDK

# set api key
erniebot.api_type = Config.api_type
erniebot.access_token = Config.access_token

models = erniebot.Model.list()

class ModelKind(Enum):
    Ernie = 'ernie-bot'
    ErnieTurbo = 'ernie-bot-turbo'
    Ernie4 = 'ernie-bot-4'

class BotRole(Enum):
    Parent = 'parent'
    Bestie = 'bestie'
    Friend = 'friend'
    Doctor = 'doctor'

    def new(role_name): 
        return BotRole(role_name)

class Bot:
    @staticmethod
    def talk(messages, model_kind: ModelKind=ModelKind.Ernie):
        response = erniebot.ChatCompletion.create(
            model=model_kind.value,
            messages=messages
        )

        return response['result']
    
    @staticmethod
    def talk_with_role(messages: List[str], bot_role: BotRole, model_kind: ModelKind=ModelKind.Ernie):
        prompts = wrap_prompt(get_prompt(bot_role))
        prompts.extend(messages)

        return Bot.talk(prompts, model_kind)

def get_prompt(bot_role: BotRole):
    match bot_role:
        case BotRole.Parent: role_name = "父母"
        case BotRole.Bestie: role_name = "闺蜜"
        case BotRole.Friend: role_name = "朋友"
        case BotRole.Doctor: role_name = "心理医生"
    
    role_prompt = f"你现在是我的{role_name}。"
    
    basic_prompt = "我现在学习、工作或者生活上有点压力，请你帮我缓解一下我和压力和焦虑。" \
        "请控制你的输出结果不要过长。"
    
    return role_prompt + basic_prompt

def wrap_prompt(prompt):
    # messages must have an odd number of elements
    return [{
        "role": "user",
        "content": prompt
    }, {
        "role": "assistant",
        "content": "好的，我知道了。"
    }]

def main():
    print(Bot.talk([{
        "role": "user",
        "content": "请问你是谁？",
    }]))

if __name__ == '__main__':
    # main()

    # print(BotRole('teacher'))
    print(BotRole.new('doctor'))
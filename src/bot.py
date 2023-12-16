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
    
    def get_label(self) -> str:
        match self:
            case BotRole.Parent: return "父母"
            case BotRole.Bestie: return "闺蜜"
            case BotRole.Friend: return "朋友"
            case BotRole.Doctor: return "心理医生"

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
        prompts = wrap_prompt(gen_prompt(bot_role))
        prompts.extend(messages)

        return Bot.talk(prompts, model_kind)

def gen_prompt(bot_role: BotRole):
    label = bot_role.get_label()
    role_prompt = f"你现在是我的{label}。"
    
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
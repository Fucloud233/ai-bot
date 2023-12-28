import erniebot
from enum import Enum
from typing import List
from pprint import pprint

from utils.config import Config
from utils.prompt import wrap_prompt, Assistant, User

# https://github.com/PaddlePaddle/ERNIE-Bot-SDK

# set api key
erniebot.api_type = Config.Erine.ApiType
erniebot.access_token = Config.Erine.AccessToken

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

    FirstPromptDefaultAnswer = "好的，我一定会控制回答字数的"
    # TODO: perfect this prompt
    ProjectPrompt = \
        "我现在学习、工作或者生活上有点压力，请你帮我缓解一下我和压力和焦虑。" \
        "请控制你的回答在20个字之间。"

    @staticmethod
    def talk(messages, model_kind: ModelKind=ModelKind.Ernie):
        try:
            response = erniebot.ChatCompletion.create(
                model=model_kind.value,
                messages=messages
            )
            
        except erniebot.errors.InvalidArgumentError as e:
            raise ValueError("messages must have an odd number of elements")
        
        return response['result']

    @staticmethod
    def talk_with_role(messages: List[str], bot_role: BotRole, model_kind: ModelKind=ModelKind.Ernie):
        prompts = wrap_prompt(gen_prompt(bot_role), Bot.FirstPromptDefaultAnswer)
        prompts.extend(messages)

        return Bot.talk(prompts, model_kind)
    
    @staticmethod
    def talk_with_custom_role(
        messages: List[str], 
        bot_role: BotRole, 
        bot_role_description: str,
        model_kind: ModelKind=ModelKind.Ernie 
    ):
        prompts = wrap_prompt(
            gen_prompt(bot_role, bot_role_description), Bot.FirstPromptDefaultAnswer
        )
        prompts.extend(messages)

        print("prompt:")
        pprint(prompts)
        
        return Bot.talk(prompts, model_kind)

# [deprecated]
def gen_prompt_old(bot_role: BotRole):
    label = bot_role.get_label()
    role_prompt = f"你现在是我的{label}。"
    
    basic_prompt = "我现在学习、工作或者生活上有点压力，请你帮我缓解一下我和压力和焦虑。" \
        "请控制你的输出结果不要过长。"
    
    return role_prompt + basic_prompt

def gen_prompt(bot_role: BotRole, bot_role_description: str=""):
    label = bot_role.get_label()

    # (1) basic role prompt 
    basic_prompt =  f"你现在是我的{label}。"
    # (2) description about role from user
    description = bot_role_description + '\n'
    # (3) some prompt about this project 
    project_prompt = Bot.ProjectPrompt

    return basic_prompt + description + project_prompt

def main():
    print(Bot.talk([{
        "role": "user",
        "content": "请问你是谁？",
    }]))

if __name__ == '__main__':
    # main()

    # print(BotRole('teacher'))
    print(BotRole.new('doctor'))
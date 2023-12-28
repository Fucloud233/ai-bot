from enum import Enum
from typing import List
from pprint import pprint
from abc import abstractmethod

from utils.prompt import wrap_prompt, BotRole

class BasicBot:
    FirstPromptDefaultAnswer = "好的，我一定会控制回答字数的"
    # TODO: perfect this prompt
    ProjectPrompt = \
        "我现在学习、工作或者生活上有点压力，请你帮我缓解一下我和压力和焦虑。" \
        "请控制你的回答在20个字之间。"

    def __init__(self):
        pass

    @abstractmethod
    def _call_api(self, messages: List[str]) -> str:
        ...

    def talk_with_role(self, messages: List[str], bot_role: BotRole):
        prompts = wrap_prompt(gen_prompt(bot_role), BasicBot.FirstPromptDefaultAnswer)
        prompts.extend(messages)

        return self._call_api(prompts)
    
    def talk_with_custom_role(
        self,
        messages: List[str], 
        bot_role: BotRole, 
        bot_role_description: str,
    ):
        prompts = wrap_prompt(
            gen_prompt(bot_role, bot_role_description), BasicBot.FirstPromptDefaultAnswer
        )
        prompts.extend(messages)

        print("prompt:")
        pprint(prompts)
        
        return self._call_api(prompts)

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
    project_prompt = BasicBot.ProjectPrompt

    return basic_prompt + description + project_prompt

from enum import Enum
from typing import List
from pprint import pprint
from abc import abstractmethod

from utils.prompt import wrap_prompt, wrap_user_prompt, BotRole
from utils.config import BotKind

class BasicBot:
    def __init__(self):
        self._summarize_context_prompt = "请用100字以内的文本概括以下我们刚刚的聊天内容。"
        self._project_prompt = "请不要主动问我问题，你只需要回答我的问题即可。并且注意控制你的回答在20个字之间。"
        self._default_answer = "好的，我一定会控制回答字数的"

        self._kind = None
        pass

    @abstractmethod
    def _call_api(self, messages: List[str]) -> str:
        ...
    
    def talk(self, history_messages: List[str], prompt: str) -> str:
        prompt = wrap_user_prompt(prompt)
        history_messages.append(prompt)
        return self._call_api(history_messages)
    
    '''
    summarize history messages to short text
    '''
    def summarize_history_messages(self, history_messages: List[str]) -> str:
        return self.talk(history_messages, self._summarize_context_prompt)

    def talk_with_role(self, messages: List[str], bot_role: BotRole):
        prompts = self.gen_prompt(bot_role)
        prompts.extend(messages)

        return self._call_api(prompts)
    
    def talk_with_custom_role(
        self,
        messages: List[str], 
        bot_role: BotRole, 
        bot_role_description: str,
        similar_context: str="",
    ):
        prompts = self.gen_prompt(bot_role, bot_role_description, similar_context)
        prompts.extend(messages)

        print("prompt:")
        pprint(prompts)
        
        return self._call_api(prompts)
    
    def gen_prompt(self, bot_role: BotRole, bot_role_description: str="", similar_context: str=""):
        label = bot_role.get_label()

        # (1) basic role prompt 
        basic_prompt =  f"假设你现在是我的{label}，请带入这个身份与我交谈。"
        # (2) description about role from user
        description = bot_role_description + '\n'
        # (3) some prompt about this project 
        project_prompt = self._project_prompt

        # GPT don't need odd number
        answer = "" if self._kind == BotKind.GPT else self._default_answer
        messages = wrap_prompt(
            basic_prompt + description + similar_context + project_prompt,
            answer
        )

        return messages

# [deprecated]
def gen_prompt_old(bot_role: BotRole):
    label = bot_role.get_label()
    role_prompt = f"你现在是我的{label}。"
    
    basic_prompt = "我现在学习、工作或者生活上有点压力，请你帮我缓解一下我和压力和焦虑。" \
        "请控制你的输出结果不要过长。"
    
    return role_prompt + basic_prompt



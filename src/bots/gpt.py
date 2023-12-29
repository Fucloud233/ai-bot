import openai
from typing import List
from pprint import pprint

from bots.base import BasicBot
from utils.config import GPTConfig, BotKind

api_key = GPTConfig.ApiKey

# Migration Guide: https://github.com/openai/openai-python/discussions/742

class GPTBot(BasicBot):
    model_type = "gpt-3.5-turbo"

    def __init__(self):
        super().__init__()
        self.client = openai.OpenAI(api_key=api_key)

        self._kind = BotKind.GPT 
    
    def _call_api(self, messages: List[str]) -> str:
        response = self.client.chat.completions.create(
            model=GPTBot.model_type,
            timeout=5,
            temperature=0.8,
            stream=False,
            messages=messages
        )

        return response.choices[0].message.content
    
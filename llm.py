import os
from openai import OpenAI

class OpenAIClient:
    history = []
    def __init__(self, api_key=None):
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def generate_chat_completion(self, messages, model="gpt-3.5-turbo"):
        return self.client.chat.completions.create(messages=messages, model=model)

    def clear_history(self):
        self.history = []

    def append_user_message(self, message):
        self.history.append({"role": "user", "content": message})

    def append_assistant_message(self, message):
        self.history.append({"role": "assistant", "content": message})


import os
from llama_index.llms.gemini import Gemini

class LLM(Gemini):
    def __init__(self):
        max_new_tokens = 512
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key is None:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        else:
            super().__init__(api_key=api_key, max_tokens=max_new_tokens, temperature=0.0)
            
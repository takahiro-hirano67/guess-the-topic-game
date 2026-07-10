"""環境変数等を管理するモジュール"""

import os

from dotenv import load_dotenv
from openai import Client

load_dotenv()

LLM_BASE_URL = os.getenv(key="LLM_BASE_URL")
LLM_API_KEY = os.getenv(key="LLM_API_KEY")
LLM_NAME = str(os.getenv(key="LLM_NAME"))

llm_client = Client(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)

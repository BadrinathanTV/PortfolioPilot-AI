# core/llm_provider.py
from langchain_openai import ChatOpenAI
from config.settings import settings


llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)


# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # API Keys
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        
        # Zerodha Credentials
        self.ZERODHA_API_KEY = os.getenv("ZERODHA_API_KEY")
        self.ZERODHA_API_SECRET = os.getenv("ZERODHA_API_SECRET")

settings = Settings()

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # LLM API 配置
    LLM_API_URL = os.getenv('LLM_API_URL', 'http://localhost:8000/v1/chat/completions')
    LLM_MODEL = os.getenv('LLM_MODEL', './Qwen2.5-14B-Instruct')
    LLM_API_KEY = os.getenv('LLM_API_KEY', '')
    
    # 聊天配置
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 2000))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    MAX_CONVERSATION_LENGTH = int(os.getenv('MAX_CONVERSATION_LENGTH', 20))
    
    # 資料庫配置
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/chatbot.db')
    
    # Flask 配置
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
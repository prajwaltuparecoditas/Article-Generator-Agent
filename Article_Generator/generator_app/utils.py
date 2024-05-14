from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


load_dotenv()
llm = ChatOpenAI()

def get_session_history(session_id: str):
    return SQLChatMessageHistory(session_id=session_id, connection_string="postgresql+psycopg2://postgres:root@localhost:5432/article_generation")
    

from langchain_core.tools import tool
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from .utils import llm

@tool
def generate_article(topic:str, context:str)->str:
  """This tool takes  parameter topic for the article  and generates the article based on that"""
  try:
    prompt = ChatPromptTemplate.from_template("Generate an article based on the following topic and context. Topic:{topic} Context: {context}")

    chain = prompt | llm
    response = chain.invoke({"topic":f"{topic}","context":f"{context}"})
    return response.content
  except Exception as e:
     print(e)
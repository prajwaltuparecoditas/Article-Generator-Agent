from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from .utils import llm, get_session_history
from .tools import generate_article

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
            "You are a helpful assistant who will help with generating articles for the users. Follow the given instructions.\
            INSTRUCTIONS:\
            1. First ask users about the topic on which he wants to generate the article on.\
            2. Ask users few questions to get revelant information about the topic.(        The question could be like:\
                 What should be the word length for the article?Who is the target audience of article? What should be tone of the article? What genre should the article be covering? ... ask only one question at a time)\
            3. Search the chat history to get topic and context\
            4. When you feel that enough context has been provided by user call the generate article function.\
            5. Do not modify the article recieved from the generate_article function, just provide the article as it is in output\
            6. Strictly provide the article recieved as a Final output"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [generate_article]

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key = "input",
    output_messages_key= "output",
    history_messages_key="chat_history",
)

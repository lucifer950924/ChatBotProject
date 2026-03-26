from langchain_core.tools import Tool
from langchain.agents import create_agent
from groq import Groq
from langchain_groq import ChatGroq
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from Utils.logger import setUpLogger
from Utils.WebSearcher import searchwithDUckDuckGO
from GoogleChatBot import GeminiChat
import os
logger,fip = setUpLogger()

os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
os.environ['OPENAI_API_BASE'] = 'https://api.deepkseek.com'
os.environ['GROQ_API_KEY'] = decryptSecretByName('GroqAPI')

RAG = GeminiChat()
logger.info('Starting to declare tools')
tools = [
    Tool(name='RAGChatbot',func = GeminiChat.generateGoogleResponse, description='Retrieval-Augmented-Genration Chatbot which shows search results from the retrieved context'),
    Tool(name='WebSearch',func = searchwithDUckDuckGO,description='Searches for user query and return the search result in string')
]
logger.info(f'Tools are declared: {tools}')


llm = ChatGroq(model='openai/gpt-oss-120b')
logger.info('LLM is declared')

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt='You are a helpful, tool-aware assistant.'
)
logger.info(f'Agent is declared {agent}')
user_query = input('Enter your query? ')
result = agent.invoke({'messages': [{'role': 'user', 'content': user_query}]})
print('Agent output:', result['messages'][1].content)

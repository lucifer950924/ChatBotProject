from AskRAGAboutPdf import AskRAGaboutPdf
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from langchain_groq import ChatGroq
from langchain.agents import initialize_agent,AgentType
import os
from Utils.logger_file import setUpLogger
logger = setUpLogger()

search = DuckDuckGoSearchRun()
logger.info('Setting Up the DuckDuckGo Search Client')
web_search_tool = Tool(
    name= 'Web Search',
    func = search.run,
    description='This is a tool to search for the user input Arguments: User Input'
)

os.environ['GROQ_API_KEY'] = decryptSecretByName('GroqAPI')
llm = ChatGroq(model='openai/gpt-oss-120b',
               temeprature = 0.3,
               verbosity = True)

logger.info(f'Setting up the llm {llm}')

tools = [web_search_tool,AskRAGaboutPdf]

agent = initialize_agent(
    tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose =True
)

logger.info(f'Setting Up the agent {agent}')

print(agent.invoke(input('Enter Name to find in SIR 2026 List: ')))
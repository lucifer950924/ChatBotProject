# from asyncio import tools
from langchain_core.tools import Tool
from langchain.agents import create_agent
from groq import Groq
from langchain_groq import ChatGroq
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from Utils.logger import setUpLogger
from Utils.WebSearcher import searchwithDUckDuckGO
from GoogleChatBot import GeminiChat
from Utils.Metrics import Metrics
from Utils.context_generation_tool import context_generator
from pydantic import BaseModel
from langchain_core.tools import StructuredTool
import os
logger,fip = setUpLogger()

os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
os.environ['OPENAI_API_BASE'] = 'https://api.deepkseek.com'
os.environ['GROQ_API_KEY'] = decryptSecretByName('GroqAPI')

class DuckDuckGoSearchInput(BaseModel):
    query: str 
class FaithfulnessInput(BaseModel):
    answer: str 
    question: str 
    threshold: float 

class AnswerRelevanceInput(BaseModel):
    answer: str 
    question: str 

class generateGoogleResponseInput(BaseModel):
    prompt: str 


class ContextRetrieverInput(BaseModel):
    prompt: str


class RunAgentInput(BaseModel):
    query: str
RAG = GeminiChat()  
metrics = Metrics()
tools = [
        StructuredTool.from_function(name='RAGChatbot',func = RAG.generateGoogleResponse, description='Retrieval-Augmented-Genration Chatbot which shows search results from the retrieved context',args_schema=generateGoogleResponseInput),
        StructuredTool.from_function(name='WebSearch',func = searchwithDUckDuckGO,description='Searches for user query and return the search result in string',args_schema=DuckDuckGoSearchInput),
        StructuredTool.from_function(name='ContextRetriever',func=context_generator,description='Takes the User Question to extract the retrieved context',args_schema=ContextRetrieverInput),
        StructuredTool.from_function(name='FaithfulnessMetrics',func=metrics._calculate_faithfulness,description='Gives the faithfulness score of the AI system. Takes input answer,question and threshold',args_schema=FaithfulnessInput),
        StructuredTool.from_function(name='AnswerRelevanceMetrics',func=metrics._calculate_answer_relevance,description='Gives the Answer Relevance score of the AI system. Takes input of answer,question',args_schema=AnswerRelevanceInput)
    ]
logger.info(f'Tools are declared: {tools}')

def run_agent(query: str) -> str:
    """Run the main agent with the given query."""
    
    logger.info('Starting to declare tools')
    


    llm = ChatGroq(model='openai/gpt-oss-120b')
    logger.info('LLM is declared')

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt='You are a helpful, tool-aware assistant.Evaluate the responses with the help of the metrics evaluation tools.RAGChatbot Tool takes the question as input argument.To calculate the faithfulness score(if RAGChatbot is used). Take the threshold as 0.3.Repond Clearly in the manner Answer: Metrics. Rules: Use the Context Retreiver Tool to retrieved the context from the present knowledge base.If the question can be aswered from the retrieved context use RAGChatBot Tool else use the WebSearch Tool to answer. If you use the RAGChatbot Tool calculate the Faithfulness and answer Relevancy using the Faithfulness Tool and the Answer Relevance Tool else only calculate the Answer Relevance using the Answer Relevance Tool .Show the responses from the tools and the calculated metrics in the final answer.After the Question is Answered correctly say "SUCCESS". Do not repeat the term "SUCCESS" in the answer.',
    )

    logger.info(f'Agent is declared {agent}')

    result = agent.invoke({'messages': [{'role': 'user', 'content': query}]})
    return result['messages'][-1].content

thinking_tools = [
    StructuredTool.from_function(name='RunAgent', func=run_agent, description='Run the main agent to answer a question', args_schema=RunAgentInput)
]

llm = ChatGroq(model='openai/gpt-oss-20b')
logger.info('Thinking LLM is declared')


thinking_agent = create_agent(
    model=llm,
    tools=thinking_tools,
    system_prompt='You will be deciding if the agent answered the question successfully or not. If the answer contains "SUCCESS" then it means the question is answered successfully. If the question is not answered successfully, you will be given the chance to ask the agent to answer the question again. You will be given the agent response and you have to decide if the question is answered successfully or not. If not, you have to ask the agent to answer the question again until you get a successful answer.RUN the agent and check if the question is answered successfully or not. If not, ask the agent to answer the question again until you get a successful answer.',
)



question = input('Enter your query? ')
result = thinking_agent.invoke({'messages': [{'role': 'user', 'content': question}]})
while 'SUCCESS' not in result['messages'][-1].content:
    logger.info('Agent is trying to answer the question again')
    result = run_agent({'messages': [{'role': 'user', 'content': result['messages'][-1].content}]})
    logger.info(f'Agent Output:{result["messages"][-1].content}')
logger.info(f'Agent Output:{result["messages"][-1].content}')
print(result['messages'][-1].content)


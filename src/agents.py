from RAGTools import convertTextstoRetriever,getContextfromRetriever,reranktheRetrievedContext,WebSearch,RAGSearch
from langchain_core.tools import StructuredTool
from pydantic import BaseModel
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
import os, sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent)
sys.path.insert(0,str(Path(__file__).parent.parent))
from Utils.initialize_api_key import setEnvironVariable
setEnvironVariable('llama')
setEnvironVariable('groq')
from langchain_groq import ChatGroq
class convertTextstoRetrieverInput(BaseModel):
    file_paths: str
    chunk_size: int = 1000
    chunk_overlap: int = 300
    embedding_model: str = "BAAI/bge-base-en-v1.5"

class getContextfromRetrieverInput(BaseModel):
    retriever: object
    query: str

class reranktheRetrievedContextInput(BaseModel):
    retriever: object = None

class WebSearchInput(BaseModel):
    query: str

class RAGSearchInput(BaseModel):
    query: str
    file_paths: str
    chunk_size: int = 1000
    chunk_overlap: int = 300
    embedding_model: str = "BAAI/bge-base-en-v1.5"

agent_model = ChatGroq(api_key = os.getenv("GROQ_API_KEY"),model= 'openai/gpt-oss-120b', temperature=0.1)

Tools = [
    StructuredTool.from_function(convertTextstoRetriever, name="convertTextstoRetriever", description="This tool takes a directory path where the text documents are stored and converts it into a retriever object by creating embeddings.", args_schema=convertTextstoRetrieverInput),
    StructuredTool.from_function(getContextfromRetriever, name="getContextfromRetriever", description="This tool takes a retriever object and a query and returns a list of relevant retrieved contexts from the retriever based on the query.", args_schema=getContextfromRetrieverInput),
    StructuredTool.from_function(reranktheRetrievedContext, name="reranktheRetrievedContext", description="This tool takes a retriever object and a query and returns a list of relevant retrieved contexts from the retriever based on the query after reranking the retrieved contexts using InfinityRerank.", args_schema=reranktheRetrievedContextInput),
    StructuredTool.from_function(WebSearch, name="WebSearch", description="This tool takes a query and returns the top 5 search results from the web based on the query.", args_schema=WebSearchInput),
    StructuredTool.from_function(RAGSearch, name="RAGSearch", description="This tool takes a query and a directory path where the text documents are stored and returns a list of relevant retrieved contexts from the retriever based on the query after reranking the retrieved contexts using InfinityRerank.", args_schema=RAGSearchInput)
]

prompt = PromptTemplate.from_template("""
You are a helpful assistant.

You have access to the following tools:

{tools}

Use the following format:

Question: {query}
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: input to the tool
Observation: result of the tool
...
Thought: I now know the final answer
Final Answer: answer to the user

{agent_scratchpad}
""")

rag_agent = create_react_agent(
    llm=agent_model,
    tools=[Tools[-1]],
    prompt=prompt
)

web_agent = create_react_agent(
    llm=agent_model,
    tools=[Tools[3]],
    prompt=prompt
)

context_agent = create_react_agent(
    llm=agent_model,
    tools=[Tools[2]],
    prompt=prompt
)

rag_executor = AgentExecutor(agent=rag_agent, tools=[Tools[-1]], verbose=True,handle_parsing_errors=True)
web_executor = AgentExecutor(agent=web_agent, tools=[Tools[3]], verbose=True,handle_parsing_errors=True)
context_executor = AgentExecutor(agent=context_agent, tools=[Tools[2]], verbose=True,handle_parsing_errors=True)

#Create Orchestrator Agent
from typing import TypedDict
class State(TypedDict):
    query: str
    response: str

def orchestrator_agent(query: str) -> str:
    '''
    This agent takes a query and returns the response based on the query by using the RAGChatBot, WebSearch and RerankedContext agents.
    Args:
        query (str): The query for which the response needs to be generated
        '''
    
    # Step 1: Use RAGChatBot agent to get the response
    context_response = context_executor.invoke({'query': query})
    if "I don't know." not in context_response['response']:
        return web_executor.invoke({'query': query})
    else:
        # Step 2: Use WebSearch agent to get the response
        rag_response = rag_executor.invoke({'query': query})
        return rag_response


from langgraph.graph import StateGraph, END, START

graph = StateGraph(
    State
)

graph.add_node("orchestrator_agent", orchestrator_agent)
graph.add_edge(START,'orchestrator_agent')
graph.add_edge('orchestrator_agent', END)

graph.add_node("rag_executor", rag_executor.invoke)
graph.add_edge(START,'rag_executor')
graph.add_edge('rag_executor', END)

graph.add_node("web_executor", web_executor.invoke)
graph.add_edge(START,'web_executor')
graph.add_edge('web_executor', END)

graph.add_node("context_executor", context_executor.invoke)
graph.add_edge(START,'context_executor')
graph.add_edge('context_executor', END)

app = graph.compile()

result = app.invoke({"query": "What is the capital of France?"})
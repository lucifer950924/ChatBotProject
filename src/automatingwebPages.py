from pathlib import Path
import os, csv, datetime,sys, subprocess
from langchain_groq import ChatGroq
from groq import Groq
from Utils.initialize_api_key import setEnvironVariable
from src.tools import write_automation_code_by_test_case, execute_generated_code, debug_code, readtheTestCasesFromCSV
from pydantic import BaseModel
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_core.prompts import PromptTemplate
from Utils.RAGChatbot import readtheTestData
setEnvironVariable('llama')
setEnvironVariable('groq')
tests = readtheTestData('TestCases.csv')

class writeCodebyTestCaseInput(BaseModel):
    test_case: str

class debugCodeInput(BaseModel):
    test_case: str
    code_file_path: str
    error_message: str

class codeRunner(BaseModel):
    filepath: str

tools =[
    StructuredTool.from_function(func=write_automation_code_by_test_case,name='writeAutomationCodeByTestCase',description='This function generates automation code based on the provided test case description using the Groq API. This acts as tool to generate code for the test cases which can be used in the automation of the test cases. The input to this function is a string which describes the test case for which automation code needs to be generated and the output is a string which is the file path of the generated code.',args_schema=writeCodebyTestCaseInput),
    StructuredTool.from_function(func=execute_generated_code,name='executeGeneratedCode',description='This function executes the generated code file and captures the output and any errors that occur during the execution. This acts as a tool to run the generated code and see the results of the test case automation. The input to this function is a string which is the file path of the generated code that needs to be executed and the output is a string which is the output of the executed code or the error message if an error occurs during execution.',args_schema=codeRunner),
    StructuredTool.from_function(func=debug_code,name='debugCode',description='This function takes the file path of the generated code and the error message as input and uses the Groq API to debug the code and fix the errors. The output of this function is the file path of the corrected code after debugging.',args_schema=debugCodeInput),
    StructuredTool.from_function(func=readtheTestCasesFromCSV,name='readTheTestCasesFromCSV',description='This function reads the test cases from a CSV file and returns a dictionary of test cases. The input to this function is the file path of the CSV file that contains the test cases and the output is a dictionary of test cases where the key is the test case name and the value is the test case description.')
]
prompt = PromptTemplate.from_template("""
Answer the following question as best you can.
Steps: Write the code -> Execute The Code -> Debug the code if there is any error -> Re-Execute the code until there is no error -> Return the final output of the code execution.
Do not use any other URL that is not specified in the test case for automation. Always use the tools when needed and follow the steps mentioned above for each test case.
Always use the URL present in the test case.
Do-Not Execute in head-less mode. Prefer Playwright
You have access to the following tools:
{tools}

Use this format:

Question: the input question
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: input to the action
Observation: result of action
Thought: I now know the final answer
Final Answer: the final answer

Question: {input}
Thought: {agent_scratchpad}
""")
# prompt = """
# You are an expert automation testing agent.

# Your responsibilities:
# 1. Generate automation code from test cases
# 2. Execute generated code
# 3. Return final verification result

# Always use tools when needed.
# """

# agent = create_agent(tools=tools, model=ChatGroq(model='openai/gpt-oss-120b'),system_prompt=prompt)

agent = create_react_agent(tools=tools, llm=ChatGroq(model='openai/gpt-oss-120b',streaming=False),prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True,max_iterations=10)

for test in tests.keys():
    try:
        print(f'Executing test case: {test}')
        result = executor.invoke({'input':tests[test]})
    # result = agent.invoke({
    # "messages": [
    #     {
    #         "role": "user",
    #         "content": tests[test]
    #     }
    # ]
    # })
        print(f'Result of the test case {test}: {result}')
    except Exception as e:
        print(f'Error occurred while executing the test case {test}: {str(e)}')


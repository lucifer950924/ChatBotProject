from pathlib import Path
import os, csv, datetime,sys,subprocess
from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
from groq import Groq
from langchain_core.prompts import ChatPromptTemplate
from Utils.initialize_api_key import setEnvironVariable
from Utils.WebElementFinder import gettheHTMLContent

def write_automation_code_by_test_case(test_case:str):
    '''
    This function generates automation code based on the provided test case description using the Groq API.
    This acts as tool to generate code for the test cases which can be used in the automation of the test cases.
    Args:
        test_case (str): A description of the test case for which automation code needs to be generated.
    Return:
        str: The file path of the generated code.
    '''

    setEnvironVariable('groq')
    # html = gettheHTMLContent()
    client = Groq()
    message = client.chat.completions.create(
        model = 'openai/gpt-oss-120b',
        messages = [
            {
                'role' : 'system',
                'content' : f'You are an Automation Enginner who writes code in Python using Automation Tools Playwright for UI Automation and Requests for API Automation and pyodbc for Database Automation.Put comments using ### in the code. Put everything other than the code in Comments ###. Do not write any explanation other than the code. Write the code in such a way that it can be run directly without any modification. The test case description is provided by the user and you have to write the code based on that.Use better methods for creating WebElements in the order id > Class > CSS > Xpath.Do not use any Github Emojis.'
            },{
                'role' : 'user',
                'content' : f'Generate automation code in python for the test case: {test_case}. The code should be in a format that can be directly used in the automation of the test case.'
            }
        ],
        temperature= 0.1,
        
    )

    parentDir = Path(__file__).parent.parent
    codeDir = parentDir / 'GeneratedCode'
    codeDir.mkdir(exist_ok = True)
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    filepath = codeDir/f'automationcode_{timestamp}.py'

    with open(filepath,'w',encoding='utf-8') as file:
        file.write(message.choices[0].message.content.replace('```python','').replace('```',''))

    return filepath

    


def execute_generated_code(filepath:str):
    '''This function executes the generated code file and captures the output and any errors that occur during the execution. This acts as a tool to run the generated code and see the results of the test case automation.
    Args:
        filepath (str): The file path of the generated code that needs to be executed.

    Return:
        str: The output of the executed code or the error message if an error occurs during execution
    '''
    try:
        parentFolder = Path(__file__).parent.parent
        pythonPath = parentFolder / 'CustomVENV' / 'Scripts' / 'python.exe'
        result = subprocess.run([pythonPath,filepath],capture_output=True,text=True,check=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while executing the generated code: {e.stderr}')


def debug_code(test_case:str,code_file_path:str,result:str):
    '''
    This function takes the test case description and runs the generated code to find if there is any error or exception in the code. This acts as a debugging tool to find any errors in the generated code.

    Args:
        test_case (str): A description of the test case for which automation code has been generated.
        code_file_path (str): The file path of the generated code that needs to be debugged.
    '''
    setEnvironVariable('groq')
    # html = gettheHTMLContent()
    client = Groq()
    with open(code_file_path,'r',encoding='utf-8') as file:
        code = file.read()
    message = client.chat.completions.create(
        model = 'openai/gpt-oss-120b',
        messages = [
            {
                'role' : 'system',
                'content' : 'You are an automation Engineer who reads the result and the code and debugs the code to find the error and fix it. Put comments using ### in the code. Put everything other than the code in Comments ###. Only write the code so that the code can be run directly without any modification. Do not write any explanation other than the code.Do not use any Github Emojis in the code.'
                f'Code : {code} error: {result} Use better methods for creating WebElements in the order id > Class > CSS > Xpath'
            },
            {
                'role' : 'user',
                'content' : f'Debug the code for the test case: {test_case} and fix the error. Provide the corrected code.'
            }

        ]
    )
    corrected_code = message.choices[0].message.content.replace('```python','').replace('```','')
    with open(code_file_path,'w',encoding='utf-8') as file:
        file.write(corrected_code)


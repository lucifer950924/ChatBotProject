from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import OllamaLLM,ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import os,time
from pathlib import Path
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName



filename = f'{int(time.time())}.txt'
currDir = os.getcwd()
exportFolder = os.path.join(currDir,'Exports',f'{int(time.time())}')
os.makedirs(exportFolder,exist_ok=True)
filepath = os.path.join(exportFolder,filename)

os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'


llm = OllamaLLM(model='llama3:latest',
                temperature = 0,
                verbose = False)

prompt = input('enter Your Prompt: ')

template = ChatPromptTemplate.from_messages([
    ('system','1.You are Automation Testing Developer \n 2.You will always give reply in Python Code \n 3.If the User asks from any other context Reply I Do not Know \n 4.Add the Documentation in Comments'),
    ('human','Write me a code to Automate {question}')
])


chain = ({'question': RunnablePassthrough()} | template | llm)

response = chain.invoke(prompt)

with open(os.path.join(exportFolder,filename),'w+',encoding='utf-8') as file:
    file.write(response)

code = response.split("```")

with open(os.path.join(exportFolder,filename.replace('.txt','.py')),'w+',encoding='utf-8') as file:
    file.write(code[1])


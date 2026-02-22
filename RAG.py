from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
import os , pathlib, asyncio , time , json , csv
from groq import Groq
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnablePassthrough
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
class RAG:
    def __init__(self):
        os.environ['GROQ_API_KEY'] = decryptSecretByName('GroqAPI')
        os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
        os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'
    def setupGroqLLM(self,prompt):
        client = Groq(api_key=os.environ['GROQ_API_KEY'])
        response = client.chat.completions.create(
            model = 'openai/gpt-oss-20b',
            messages= [
                {
                    'role' : 'system',
                    'content' : 'You are a helpful assistant for answering questions based on the provided context.End your answer with a follow up question to keep the conversation going.'
                },
                {
                    'role' : 'user',
                    'content' : f'{prompt}'
                }
                

            ],
            temperature = 0.3,
            reasoning_effort='medium',
            stream = False
        )

        return response.choices[0].message.content
    

    def setupLLAMALLM(self,prompt):
        llm = OllamaLLM(
            model = 'phi3:mini',
            temperature = 0.3,
            verbosity = True
        )

        template = ChatPromptTemplate.from_messages(
            [
                ('system' , 'You are a helpful assistant for answering questions based on the provided context.End your answer with a follow up question to keep the conversation going.'),
                ('human' , '{question}')
            ]
        )

        chain = ({'question' : RunnablePassthrough()} | template | llm)

        response = chain.invoke(prompt)

        return response
    

    def chat_Between_LLms(self,initial_prompt):
        prompt = initial_prompt
        iter = 0
        response = ''
        while iter < 10:
            response_groq = self.setupGroqLLM(prompt)
            print(f'Groq Response: {response_groq}')
            response_ollama = self.setupLLAMALLM(response_groq)
            print(f'Ollama Response: {response_ollama}')
            prompt = response_ollama
            iter += 1
            response += f'Iteration {iter}:\nGroq: {response_groq}\nOllama: {response_ollama}\n\n'

        ExportDir = os.path.join(os.getcwd(),'Exports',f'{int(time.time())}')
        os.makedirs(ExportDir, exist_ok=True)
        with open(os.path.join(ExportDir,'LLM_Chat_Export.txt'),'w',encoding = 'utf-8') as f:
            f.write(response)




x = RAG()
# initial_prompt = input('Enter your prompt for the LLMs to start the conversation: ')
initial_prompt = 'Will AI replace Humans?'
x.chat_Between_LLms(initial_prompt)
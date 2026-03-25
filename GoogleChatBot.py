from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
import os, pathlib,datetime,logging,subprocess, time
from langchain_community.document_loaders import DirectoryLoader,TextLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from Utils.logger import setUpLogger
from Utils.cache_embeddings import cacheEmbeddings
from Utils.Metrics import Metrics
import numpy as np
logger , fip = setUpLogger()
class GeminiChat:
    def __init__(self):
        
        os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
        os.environ['OPENAI_API_BASE'] = 'https://api.deepkseek.com'
        self.llm = ChatOllama(model='phi3:mini',
                                          temperature = 0.3,
                                          verbose = True)
        
        
    def generateGoogleResponse(self,prompt):
        
        CorpusTextDir = os.path.join(os.getcwd(),'Corpus')
        logger.info(f'Starting to Split Documents')
        # docs = list(map(lambda x:DirectoryLoader(x,glob='**/*.pdf',loader_cls=PyPDFLoader,loader_kwargs={'encoding':'utf-8'}).load_and_split(),CorpusTextDir))[0]
        fps = list(pathlib.Path(CorpusTextDir).iterdir())
        filenames = [str(i.name).replace('.pdf','') for i in fps if i.is_file()]
        embeddings = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")
        for fp in filenames:
            fpath = os.path.join(os.getcwd(),'cache',fp)
            if os.path.exists(fpath):
                texts = np.load(os.path.join(fpath,fp,'texts.npy'))
                vectors = np.load(os.path.join(fpath,fp,'vectors.npy'))
                logger.info(f'Loading the Vectors {vectors} , {texts}')
                text_vector = list(zip(texts,vectors))
                db = FAISS.from_embeddings(text_vector,embedding=embeddings)
                logger.info('DataBase Loaded successfully')
            else:

                loader = PyPDFLoader(file_path = os.path.join(os.getcwd(),'Corpus',f'{fp}.pdf'))
                docs = loader.load_and_split()
                logger.info(f'Documents are splitted {docs}')
                db = FAISS.from_documents(documents=docs,embedding=embeddings)
                context = [doc.page_content for doc in docs]
                vectors = embeddings.embed_documents(context)
                logger.info(f'Saving the context Vector {vectors} , {context}')
                os.makedirs(os.path.join(fpath,fp),exist_ok=False)
                np.save(os.path.join(fpath,fp,'vectors.npy'),vectors)
                np.save(os.path.join(fpath,fp,'texts.npy'),context)
        logger.info(f'Vector Database is setup {db}')
        retriever = db.as_retriever(search_kwargs = {'k':4})
        logger.info(f'retriever is setup {retriever}')

        template = ChatPromptTemplate.from_messages([
            ('system','You are a Heplful assistant and a subject expert. Answer from the retrieved documents only. If user asks from out of context, answer"I dont know"'),
            ('human','{question}')
        ])
        

        chain = ({'context': retriever,'question':RunnablePassthrough()} | template | self.llm)
        logger.info(f'chain is setup successfully {chain}')
        return chain.invoke(prompt).content,retriever 

    
        
x = GeminiChat()
logger.info('Chat Bot is initialized')
response ,  retriver = x.generateGoogleResponse('Who is Eragon?')
logger.info(f'Chatbot is giving response successfully {response}')
metrics = Metrics()
logger.info('Metrics Calculation is starting')
docs = retriver.invoke('Who is Eragon?')
context = "\n".join([doc.page_content for doc in docs])
logger.info(f'Metrics is calculated : {metrics._calculate_faithfulness(response,context,0.5)}')
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader,WebBaseLoader,DirectoryLoader,TextLoader
from langchain_community.vectorstores import FAISS,Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
import os,time,requests,json,sys,pathlib,re,json
import streamlit as st


def RAGOllama(userPrompt: str):
    curr_dir = os.getcwd()
    sys.path.append(os.path.join(curr_dir,'Utils'))
    from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName as decN

    os.environ['OPENAI_API_KEY'] = decN('RAGChatBot_deepseek')
    os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'

    #### Read the doc

    databasePath = os.path.join(curr_dir,'Database')
    documents = []
    chunks = []
    os.makedirs(os.path.join(curr_dir,'Vectors'),exist_ok=True)

    vectorPath = os.path.join(curr_dir,'Vectors') 
    splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 200)
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    zipTexts = []
    zipVectors = []
    for path in pathlib.Path(databasePath).iterdir():
        vectorFilePath = os.path.join(vectorPath,f'{str(path).split(os.sep)[-1]}_Vectors.json')
        if os.path.exists(vectorFilePath):
            with open(vectorFilePath,'r',encoding='utf-8') as file:
                data = json.load(file)
            texts = data['chunks']
            vector = data['vectors']
            if pathlib.Path(vectorFilePath).is_file():
                for ele in texts:
                    zipTexts.append(ele)
                for ele in vector:
                    zipVectors.append(ele)
            
        else:
            filename = f'{str(path).split(os.sep)[-1]}.txt' 
            loader = TextLoader(os.path.join((str(path)),filename),encoding='utf-8')
            doc = loader.load()
            chunk = splitter.split_documents(doc)
            chunks.extend(chunk)
            
            texts = [ele.page_content for ele in chunks]
            vector = embeddings.embed_documents(texts)
            with open(vectorFilePath,'w',encoding='utf-8') as file:
                json.dump(
                    {
                        'chunks' : texts,
                        'vectors' : vector
                    },
                    file
                )
        
    text_embedding_pairs = zip(zipTexts,zipVectors)         
    # text_embedding_pairs = zip(texts,vector)
    db = FAISS.from_embeddings(text_embedding_pairs,embedding=embeddings)
    retriever = db.as_retriever(search_kwargs = {'k':4})
    chatTemplate = ChatPromptTemplate.from_messages([
        (
            "system","You are an AI Assistant \n You will always answer from context \n If the question is not from context \n Say : I do not know."
        ),
        (
            "human","\nContext: {context}"
            "question : {question}"
        )
    ])

    llm = ChatOllama(model = 'llama3:latest',
                    temperature= 0.3,
                    verbose = True)

    chain = ({'context': retriever,'question':RunnablePassthrough()} | chatTemplate | llm)


    response = chain.invoke(userPrompt)

    return response.content




import os, time , pathlib, subprocess, tracemalloc, asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaLLM
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnablePassthrough

dataCollectorPath = pathlib.Path(os.path.join(os.getcwd(),'Utils'))
for path in dataCollectorPath.iterdir():
    if path.is_file() and path.name == 'crawlURL.py':
        subprocess.run(['python',str(path)])


def RAG(prompt=''):
    os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
    os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'
    cwd = os.getcwd()
    databasePath = pathlib.Path(os.path.join(cwd,'Database'))
    dataPath = [pathlib.Path(path) for path in databasePath.iterdir()]
    datafilePath = []

    for path in dataPath:
        filepath = list(path.iterdir())[0]

        if pathlib.Path(filepath).is_file() and pathlib.Path(filepath).suffix == '.txt':
            datafilePath.append(str(filepath))

    splitter = CharacterTextSplitter(chunk_size = 800, chunk_overlap = 200)
    docs = []
    for path in datafilePath:
        loader = TextLoader(path)
        document = loader.load()
        docs.append(document)

    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")

    db = FAISS.from_documents(chunks,embedding=embeddings)
    retreiver = db.as_retriever(search_kwargs = {'k':3})

    llm = ChatOllama(
        model='llama3:latest',
        temperature= 0.3,
        verbose=True
    )
    ChatTemplate = ChatPromptTemplate.from_messages(
        [
            ('system','You assume the role of a subject expert.'
            'Rule:'
            '1. Answer questions from the context only 2. If The question is out of context Answer "I Do not Know" 3. Run the Prompts 3 times and generate 3 response'),
            ('human','Your response is as follows:')
        ]
    )

    chain = ({'context': {retreiver},'question': RunnablePassthrough()} | ChatTemplate | llm)

    return chain.invoke(prompt)

print(RAG('Tell me about 5 important events in Cold War'))




        
    

        


import os, time , pathlib, subprocess, tracemalloc, asyncio, subprocess, csv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaLLM
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnablePassthrough
# from Utils import crawlURL,readPdf
from langchain.tools import tool
# from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents import create_agent
os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
os.environ['OPENAI_API_BASE'] = 'https://api.deepdeek.com'
UtilToolName = { 'crwal': 'crawlURL.py','read':'readPdf.py'}


def RunTool(act):
    ''' This Function runs the programs present in Utils directory as needed.'''
    Utildir = pathlib.Path(os.path.join(os.getcwd(),'Utils'))
    tool = UtilToolName[act]
    file = (str(fp) for fp in list(Utildir.iterdir()) if fp.name == tool)
    return subprocess.run(['py','-3.10',next(file)])


def create_RetrieverTool():
    '''This function creates a retriever tool'''
    database_dir = os.path.join(os.getcwd(),'Database')
    listOfDatabases = list(map(lambda x:os.path.join(str(database_dir),str(x),f'{str(x)}.txt'),os.listdir(database_dir)))
    chunks = []
    splitter = CharacterTextSplitter()
    embeddings = HuggingFaceEmbeddings(model = 'sentence-transformers/all-miniLM-L6-v2')
    try:
        for fp in listOfDatabases:
            if os.path.exists(fp):
                # Loads the documents
                loader = TextLoader(fp,encoding='utf-8')
                documents = loader.load()
                chunks.extend(splitter.split_documents(documents))
                
        db = FAISS.from_documents(chunks,embedding=embeddings)
        return db.as_retriever(search_kwargs = {'k':4})
    except OSError:
        print('Database File Doesnot exist')

def RAG(prompt):
    # RunTool('read')
    retriever = create_RetrieverTool()
    llm = OllamaLLM(
        model = 'phi3:mini',
        temperature = 0.3,
        verbosity = True
    )
    template = ChatPromptTemplate.from_messages([
        ('system','Rules 1. You take the role of subject expert 2. Respond from the retrieved docs 3. If the context is not present say I donot know.'),
        ('human','Context:{context}\n Question:{question}')
    ]
    )
    chain = ({'context': retriever,'question':RunnablePassthrough()} | template | llm)

    retrieved_docs = retriever.invoke(prompt)
    context = '\n\n'.join(doc.page_content for doc in retrieved_docs)

    return {'question': prompt,'answer': chain.invoke(prompt),'contexts':context}




    







        
    

        


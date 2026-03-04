from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from groq import Groq
import os, time, datetime, pathlib
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from Utils.ConvertPdfTotext import convertImagetoText
from EvaluateRAG import evalRAGDeepEval,evalRAGRAGAS

@evalRAGRAGAS
def AskRAGaboutPdf(name):
    os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
    os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'
    os.environ['GROQAI_API_KEY'] = decryptSecretByName('GroqAPI')
    databasePath = os.path.join(os.getcwd(),'DataBase')
    texts = ""
    databasePath =pathlib.Path(databasePath)
    list_of_fp = [str(fp) for fp in list(databasePath.iterdir()) if fp.is_file() and fp.suffix == ".pdf"]
    bengali_translator_client = Groq(
        api_key = os.environ['GROQAI_API_KEY']
    )
    for fp in list_of_fp:
        filename = fp.split("\\")[-1]
        filename = filename.split(".")[0]
        print(filename)
        if not os.path.exists(os.path.join(os.getcwd(),"KnowledgeExports",f"{filename}.txt")):
            os.makedirs(os.path.join(os.getcwd(),"KnowledgeExports"),exist_ok = True)
            text = convertImagetoText(fp)
            with open(os.path.join(os.getcwd(),"KnowledgeExports",f"{filename}.txt"),'w',encoding='utf-8') as file:
                file.write(text)
            texts += text + '\n'
        else:
            continue


    
    response = bengali_translator_client.chat.completions.create(
        model = 'openai/gpt-oss-20b',
        messages = [
            {
                'role' : 'system',
                'content' : 'You are a English To Bengali Translater. Translate the texts from English To Bengali. Generate all possible spellings of the name given'
            },
            {
                'role' : 'user',
                'content' : f'Please Translate the following name from English to Bengali. name: {name}'
            }
        ],
        temperature= 0,
        reasoning_effort= 'low'
    )

    name_in_bengali = response.choices[0].message.content
    
    ### Load the PDF Docs
    loader = DirectoryLoader(path=os.path.join(os.getcwd(),'KnowledgeExports'),glob = '**/*.txt',loader_cls = TextLoader,loader_kwargs={'encoding':'utf-8'})
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 200)
    chunks = splitter.split_documents(documents)
    vectors = FAISS.from_documents(chunks,embedding=HuggingFaceEmbeddings(model = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'))

    retriever = vectors.as_retriever(search_kwargs = {'k': 3})

    prompt_template = ChatPromptTemplate([
        ('system','You are an retriever assistant. Rules: 1) Always Search for the name from the document present 2) Return the results as Your Name is present in the SIR 2026 List. Return the Id Number EPIC Number and all the details under this Name'),
        ('user','Please find the name in the SIR 2026 list and Retrieve all the details for the name {question}')
    ])

    retrieverllm = OllamaLLM(model = 'phi3:mini',
        temperature = 0.2,
        verbosity = True)


    chain = ({'context': retriever,'question': RunnablePassthrough()} | prompt_template | retrieverllm)

    

    return chain.invoke(name_in_bengali),retriever

print(AskRAGaboutPdf(input('Enter Name to find in SIR 2026 List: ')))

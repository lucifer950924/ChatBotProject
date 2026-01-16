import os
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName as decN
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from docx import Document
from time import time
from pathlib import Path
from DocToPDF import docxToPdf
def splitTheKnowledgeBase():
    ### Declare the Current Working Directory

    currDir = os.getcwd()
    datbaseDir = os.path.join(currDir,"Database")

    ### Load the documents
    try:
        loader = DirectoryLoader(datbaseDir,glob="**/*.pdf",loader_cls=PyPDFLoader)
        documents = loader.load()
        
    except Exception:
        print("Document is not loaded! Please Check!")
    ## Document is loaded

    ### split the text

    splitter = RecursiveCharacterTextSplitter(chunk_size = 800,chunk_overlap = 200)
    chunks = splitter.split_documents(documents)

    return chunks

def EmbedTheChunks(chunks:list):
    ### Embed and store the chunks in a Vector


    embeddings = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks,embedding=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k":3})
    return retriever

def RAGChatbot(prompt: str,retrieve):
    ### Save the environment variables
    deep_seek_key = decN("RAGChatBot_deepseek")

    os.environ['OPENAI_API_KEY'] = deep_seek_key
    os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'
    

    
    ##Creating LLM Model
    llm = ChatOllama(
        model="llama3:latest",
        temperature = 0.5,
        verbose = True
        )

    ## Create Context for RAG
    query = prompt
    docs = retrieve.invoke(query)
    context = "\n\n".join(doc.page_content for doc in docs)
    response = llm.invoke([
        HumanMessage(
            content = f"""
                    I am your Knowledge Base. Ask me!
                    Context:  {context}
                    Question: {query}
                """

            )

        ])

    return response.content


if __name__ == "__main__":
    
    chunks = splitTheKnowledgeBase()
    retriever = EmbedTheChunks(chunks)
    
    while True:
        userPrompt = input("Hi! Ask me anything about your knowledge base: \n")
        if userPrompt.lower() == 'exit':
            break
        else:
            response = None
            while response == None:
                print("Reading The Books......Wait Please.....")
                response = RAGChatbot(userPrompt,retriever)
                print(response)
                currDir = os.getcwd()
                timestamp = int(time())
                os.makedirs(os.path.join(currDir,"Output",str(timestamp)),exist_ok=True)
                fileNames = [file.name for file in Path(os.path.join(currDir,"Database")).glob('*.pdf')]
                doc = Document()
                doc.add_paragraph(response)
                doc.save(os.path.join(currDir,"Output",str(timestamp),f"{fileNames[0]}_{timestamp}.docx"))
                docxToPdf(os.path.join(currDir,"Output",str(timestamp),f"{fileNames[0]}_{timestamp}.docx"))
                print("****Mischeif Managed*****")
        



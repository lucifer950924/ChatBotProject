from playwright.async_api import async_playwright
import os, time, requests, csv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader

def readtheTestData():
    currdir = os.getcwd()
    testdataDir = os.path.join(currdir,'TestData','RunTimeData.csv')
    data = {}
    with open(testdataDir,'r',encoding='utf-8') as file:
        read = csv.reader(file)
        for row in read:
            data[row[0]] = row[-1]

    # response = requests.get('https://potterapi-fedeperin.vercel.app/en/books')
    # print(response.text)
    return data





def importTheFiles():
    ### Supported Formats ####
    currdir = os.getcwd()
    dataDir = os.path.join(currdir,'Database')
    listofFiles = [str(path) for path in list(Path(dataDir).iterdir()) if path.is_file]
    listOfDocs = []
    for file in listofFiles:
        if '.pdf' in file:
            loader = DirectoryLoader(dataDir,glob="**/*.pdf",loader_cls=PyPDFLoader)
            docs = loader.load()
            listOfDocs.append(docs)
        elif '.docx' in file:
            loader = DirectoryLoader(dataDir,glob="**/*.docx",loader_cls=Docx2txtLoader)
            docs = loader.load()
            listOfDocs.append(docs)
        elif '.txt' in file:
            loader = DirectoryLoader(dataDir,glob="**/*.txt",loader_cls=TextLoader)
            docs = loader.load()
            listOfDocs.append(docs)

    return listOfDocs
    
def SplitTheText():
    listofDocs = importTheFiles()
    splitter = RecursiveCharacterTextSplitter(chunk_size = 800,chunk_overlap = 200)
    for textDocs in listofDocs:
        chunks = splitter.split_documents(textDocs)
    return chunks


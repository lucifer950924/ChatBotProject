import os, sys
from pathlib import Path
sys.path.append(Path(__file__).parent.parent)
sys.path.insert(0,str(Path(__file__).parent.parent))
from Utils.initialize_api_key import setEnvironVariable
map(setEnvironVariable, ['llama', 'groq'])
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ddgs import DDGS
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

def convertTextstoRetriever(file_paths: str,chunk_size:int=1000,chunk_overlap:int = 300,embedding_model: str="BAAI/bge-base-en-v1.5") -> object:
    ''''
    Loads the text documents in the directory and converts it into chunks and then converts into a retriever object by creating embeddings
    This tool automatically detects the file format and uses the appropriate loader to load the documents. It supports .txt, .pdf, and .docx file formats.
    Args:
        file_paths (str): The directory path where the text documents are stored
        chunk_size (int, optional): The size of each chunk. Defaults to 1000.
        chunk_overlap (int, optional): The overlap between chunks. Defaults to 300.
        embedding_model (str, optional): The name of the embedding model to use. Defaults to "BAAI/bge-base-en-v1.5".

    Returns:
        retriever: The retriever object created from the text documents
    '''
    # Load the documents from the directory
    supported_formats = {
        '.txt' : TextLoader,
        '.pdf' : PyPDFLoader,
        '.docx' : Docx2txtLoader
    }
    files_path = Path(file_paths).iterdir()
    chunks = []
    for file in files_path:
        
        if file.suffix in supported_formats.keys():
            loader_cls = supported_formats[file.suffix]
            loader =  DirectoryLoader(file_paths, glob=f"**/*{file.suffix}",loader_cls = loader_cls)
            # Split the documents into chunks
            chunks.extend(loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)))
    # Create the embeddings and the retriever
    embedding_model = HuggingFaceEmbeddings(model_name = embedding_model)
    db = FAISS.from_documents(chunks, embedding_model)
    retriever = db.as_retriever(search_kwargs = {'k': 20})
    return retriever

def getContextfromRetriever(retriever: object , query: str) -> list:
    '''
    This tool takes a retriever object and a query and returns a list of relevant retrieved contexts from the retriever based on the query.
    Args:
        retriever (object): The retriever object created from the text documents
        query (str): The query for which the relevant contexts need to be retrieved

    Returns:
        list: A list of relevant retrieved contexts from the retriever based on the query    
    '''
    if not retriever:
        fp = Path(__file__).parent.parent / 'Knowledgebase'
        retriever = convertTextstoRetriever(file_paths = str(fp))
    context = retriever.invoke(query)
    return [doc.page_content for doc in context]
    
def reranktheRetrievedContext(retriever: object = None) -> object:
    '''
    This tool takes a retriever object and returns reranked retrieved contexts using a cross-encoder model.
    Args:
        retriever (object): The retriever object created from the text documents

    Returns:
        object: A wrapper with an invoke method that returns reranked documents
    '''
    if retriever is None:
        fp = Path(__file__).parent.parent / 'Knowledgebase'
        retriever = convertTextstoRetriever(file_paths = str(fp))    
    
    cross_encoder_model = HuggingFaceCrossEncoder(model_name = "cross-encoder/ms-marco-MiniLM-L-6-v2")
    
    # Create a wrapper retriever that reranks results
    class RerankedRetriever:
        def __init__(self, base_retriever, reranker, top_n=5):
            self.base_retriever = base_retriever
            self.reranker = reranker
            self.top_n = top_n
        
        def invoke(self, query: str):
            docs = self.base_retriever.invoke(query)
            pairs = [(query, doc.page_content) for doc in docs]
            scores = self.reranker.score(pairs)
            # Sort by score descending and return top_n
            ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
            return [doc for doc, score in ranked[:self.top_n]]
    
    return RerankedRetriever(retriever, cross_encoder_model, top_n=5)

def WebSearch(query: str) -> str:
    '''
    This tool takes a query and returns the top 5 search results from the web based on the query.
    Args:
        query (str): The query for which the search results need to be retrieved

    Returns:
        str: The top 5 search results from the web based on the query
    '''
    with DDGS() as ddgs:
        results = ddgs.text(
            query,
            region='wt-wt',
            safesearch='Off',
            timelimit='h',
            max_results=5
        )

    return [result['body'] for result in results]


def RAGSearch(query: str) -> list:
    '''
    This tool takes a query and a directory path where the text documents are stored and returns a list of relevant retrieved contexts from the retriever based on the query after reranking the retrieved contexts using InfinityRerank.
    Args:
        query (str): The query for which the relevant contexts need to be retrieved
        file_paths (str): The directory path where the text documents are stored

    Returns:
        list: A list of relevant retrieved contexts from the retriever based on the query after reranking the retrieved contexts using InfinityRerank
    '''
    fp = Path(__file__).parent.parent / 'Knowledgebase'
    ret = convertTextstoRetriever(file_paths = str(fp))
    reranked_ret = reranktheRetrievedContext(ret)
    context = getContextfromRetriever(reranked_ret, query)
    return context
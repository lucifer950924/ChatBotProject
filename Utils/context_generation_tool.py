import pathlib,os
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
from langchain_community.vectorstores import FAISS
def context_generator(prompt):
    '''
    Takes the retriever object and generates the context

    Args:
        prompt: Takes the User question as argument

    Retruns:
        returns the context as string

    '''
    CorpusTextDir = os.path.join(os.getcwd(),'Corpus')
    
       
    fps = list(pathlib.Path(CorpusTextDir).iterdir())
    filenames = [str(i.name).replace('.pdf','') for i in fps if i.is_file()]
    embeddings = HuggingFaceEmbeddings(model = "sentence-transformers/all-MiniLM-L6-v2")
    for fp in filenames:
        fpath = os.path.join(os.getcwd(),'cache',fp)
        if os.path.exists(fpath):
            texts = np.load(os.path.join(fpath,fp,'texts.npy'))
            vectors = np.load(os.path.join(fpath,fp,'vectors.npy'))
            
            text_vector = list(zip(texts,vectors))
            db = FAISS.from_embeddings(text_vector,embedding=embeddings)

    retriever = db.as_retriever(search_kwargs = {'k':4})

    docs = retriever.invoke(prompt)

    context = " ".join([doc.page_content for doc in docs])

    return context


import os, pathlib, time
from datetime import datetime

class cacheEmbeddings:
    def __init__(self,embeddings):
        self.embeddings =embeddings
        self.cwd = os.getcwd()
        self.timestamp = datetime.now().strftime('%Y%m%d%H%S')

    def cacheEmbeddingsinfolder(self,filename):
        cache_dir = os.path.join(self.cwd,'cache',f'{filename}')
        os.makedirs(cache_dir,exist_ok=True)
        cacheName = f'{filename}.txt'
        cachefp = os.path.join(cache_dir,cacheName)

        with open(cachefp,'w',encoding = 'utf-8') as files:
            files.write(self.embeddings)

        return cachefp
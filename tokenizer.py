import sentencepiece as spm
from datasets import load_dataset
import os, pathlib
class Tokenizer:
    def __init__(self):
        cwd = os.getcwd()
        corpusDir = os.path.join(cwd,'CorpusText')
        corpusDir = list(map(lambda x: pathlib.Path(os.path.join(corpusDir,x)),os.listdir(corpusDir)))
        data = ''
        for fp in corpusDir:
            if fp.is_file() and fp.suffix == '.txt':        
                with open(fp,'r',encoding = 'utf-8') as file:
                    data += file.read()
        
        os.makedirs(os.path.join(cwd,'CorpusData'),exist_ok = True)
        dataPath = os.path.join(cwd,'CorpusData','output.txt')

        with open(dataPath,'w',encoding='utf-8') as file:
            file.write(data)
        


        spm.SentencePieceTrainer.Train(
            input = dataPath,
            model_prefix = 'tokenizer',
            vocab_size = 8000 
        )

    
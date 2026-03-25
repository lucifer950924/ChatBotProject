import os,pathlib,time, datetime
from pypdf import PdfReader
from pdfminer.high_level import extract_text
import pytesseract
from pdf2image import convert_from_path
def readpdfCorpus():
    currDir = os.getcwd()
    corpusDirPath = pathlib.Path(os.path.join(currDir,'Corpus'))
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%S')
    os.makedirs(os.path.join(currDir,'CorpusText',timestamp),exist_ok=True)
    CorpusTextDir = os.path.join(currDir,'CorpusText',timestamp)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    for fp in list(corpusDirPath.iterdir()):
        data = ''
        if fp.is_file() and fp.suffix == '.pdf':
            imgs = convert_from_path(fp)
            for img in imgs:
                text = pytesseract.image_to_string(img)
                data += text
            with open(os.path.join(CorpusTextDir,str(fp.name).replace(".pdf",".txt")),'w+',encoding='utf-8') as file:
                file.write(data)


readpdfCorpus()

                
            

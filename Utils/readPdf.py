import os , re, tracemalloc, asyncio, requests
from RAGChatbot import readtheTestData
from io import BytesIO
from pypdf import PdfReader

texts = []

async def read_pdf(url=None):
    tracemalloc.start()
    try:
        
        currDir = os.getcwd()
        url_name = ''.join(re.findall(r'[A-Za-z]+',url))
        os.makedirs(os.path.join(currDir,'Database',f'Database_{url_name}'),exist_ok=True)
        path = os.path.join(currDir,'Database',f'Database_{url_name}',f'Database_{url_name}.txt')
        read_flag =False
        if os.path.exists(path):
            with open(path,'r',encoding='utf-8') as file:
                read_text = file.read()
            if len(read_text) == 0:
                read_flag = True
            else:
                print('Skipping the read')
        else: 
            read_flag = True

        if read_flag:   
            response = requests.get(url)
            if response.status_code == 200:
                file = BytesIO(response.content)
                reader = PdfReader(file)
                for page in reader.pages:
                    texts.append(page.extract_text())        
    except Exception as e:
        print('Waiting for too long.')
    finally:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(texts))


data = readtheTestData()
URL = data['readPDFLink']
asyncio.run(read_pdf(URL))
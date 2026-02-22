from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os , re, tracemalloc, asyncio
from RAGChatbot import readtheTestData


visited = set()
texts = []

async def crawl(page, url,base_domain):
    if url in visited:
        return
    visited.add(url)

    await page.goto(url,timeout = 20000)
    await page.wait_for_load_state('networkidle')


    soup = BeautifulSoup(await page.content(), 'html.parser')
    text = soup.get_text(separator="\n")
    title = await page.title()
    texts.append(f'{title} \n {text}')
    for a in soup.find_all('a', href=True):
        nexturl = urljoin(url, a['href'])
        if urlparse(nexturl).netloc == base_domain:
            await crawl(page,nexturl,base_domain)


async def crawl_url(url=None):
    tracemalloc.start()
    try:
        
        currDir = os.getcwd()
        url_name = ''.join(re.findall(r'[A-Za-z]+',url))
        os.makedirs(os.path.join(currDir,'Database',f'Database_{url_name}'),exist_ok=True)
        path = os.path.join(currDir,'Database',f'Database_{url_name}',f'Database_{url_name}.txt')
        crawl_flag =False
        if os.path.exists(path):
            with open(path,'r',encoding='utf-8') as file:
                read_text = file.read()
            if len(read_text) == 0:
                crawl_flag = True
            else:
                print('Skipping the crawl')
        else: 
            crawl_flag = True

        if crawl_flag:   
            
            async with async_playwright() as p:
                    
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()
                start_url = url
                domain = urlparse(start_url).netloc

                await crawl(page, start_url, domain)

                await browser.close()
        

            
            
    except Exception as e:
        print('Waiting for too long.')
    finally:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(texts))


data = readtheTestData()
URL = data['crawlURLLink']
asyncio.run(crawl_url(URL))
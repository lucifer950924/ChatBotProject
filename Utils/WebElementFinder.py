from playwright.sync_api import sync_playwright
import os, asyncio, json
from pathlib import Path
from Utils.RAGChatbot import readtheTestData


def gettheHTMLContent():
    '''
    This function uses Playwright to launch a headless browser
    and navigate to a specific URL to retrieve all the HTML content of the page.

    Output:
        list: A list of dictionaries where each dictionary contains details about an interactive element on the page, including its tag name, text content, id, class name, type, name, placeholder, and XPath.
    
    '''
    data = readtheTestData()
    url = data.get('URL')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        elements = page.evaluate("""
    () => {
        const elements = [];

        document.querySelectorAll('input, h1, h2, h3, button, a, select, textarea').forEach(el => {
            elements.push({
                tag: el.tagName,
                text: el.innerText || '',
                id: el.id || '',
                name: el.name || '',
                placeholder: el.placeholder || ''
            });
        });

        return elements;
    }
    """)

        browser.close()

    currDir = Path(__file__).parent.parent
    DomBodypath = currDir / 'urlDOMs' 
    DomBodypath.mkdir(exist_ok=True)
    DomBodypath = DomBodypath / f'{data.get("URL")}'.strip('https://').strip('http://').replace('.','_')
    DomBodypath.mkdir(exist_ok=True)
    with open(DomBodypath / 'DomBody.json','w',encoding = 'utf-8') as file:
        json.dump(elements,file,indent=4)

    return DomBodypath / 'DomBody.json'

def readtheJsonBody():
    '''
    This function reads the JSON file that contains the details of interactive elements on the web page and returns the data as a list of dictionaries.
    Output:
        Exports a .json of the DOM body of the webpage which contains details about all the interactive elements on the page, including their tag name, text content, id, class name, type, name, placeholder, and XPath. The function returns this data as a list of dictionaries where each dictionary represents an interactive element on the page.
    Returns:
         list: A list of dictionaries where each dictionary contains details about an interactive element on the page, including its tag name, text content, id, class name, type, name, placeholder, and XPath.
    '''
    file_path = gettheHTMLContent()
    with open(file_path,'r',encoding='utf-8') as file:
        data = json.load(file)

    return data





    


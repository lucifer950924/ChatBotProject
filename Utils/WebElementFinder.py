from playwright.sync_api import sync_playwright
import os, asyncio
from Utils.RAGChatbot import readtheTestData


def gettheHTMLContent():
    '''
    This function uses Playwright to launch a headless browser
    and navigate to a specific URL to retrieve all the HTML content of the page.

    Return:
        str: The HTML content of the page.
    
    '''
    data = readtheTestData()
    url = data.get('URL')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        elements = page.evaluate("""
() => {
    const selectors = [
        'button',
        'a',
        'input',
        'textarea',
        'select',
        '[role="button"]',
        '[onclick]',
        '[tabindex]'
    ];

    const nodes = document.querySelectorAll(selectors.join(','));

    return [...nodes]
        .filter(el => {
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();

            return (
                style.display !== 'none' &&
                style.visibility !== 'hidden' &&
                style.opacity !== '0' &&
                !el.disabled &&
                rect.width > 0 &&
                rect.height > 0
            );
        })
        .map(el => ({
            tag: el.tagName,
            text: el.innerText || el.value || '',
            id: el.id || '',
            className: el.className || '',
            type: el.type || '',
            name: el.name || '',
            placeholder: el.placeholder || '',
            xpath: getXPath(el)
        }));

    function getXPath(element) {
        if (element.id)
            return `//*[@id="${element.id}"]`;

        let path = [];
        while (element && element.nodeType === 1) {
            let index = 1;
            let sibling = element.previousElementSibling;

            while (sibling) {
                if (sibling.tagName === element.tagName) index++;
                sibling = sibling.previousElementSibling;
            }

            path.unshift(`${element.tagName.toLowerCase()}[${index}]`);
            element = element.parentElement;
        }

        return '/' + path.join('/');
    }
}
""")

        browser.close()

    return elements


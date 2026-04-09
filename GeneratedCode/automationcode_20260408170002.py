
### Import Playwright sync API ###
from playwright.sync_api import sync_playwright

### Main execution function ###
def run():
    ### Start Playwright context ###
    with sync_playwright() as p:
        ### Launch Chromium browser (set headless=False for visual debugging) ###
        browser = p.chromium.launch(headless=False)
        ### Open a new page/tab ###
        page = browser.new_page()
        ### Navigate to the application under test – replace with actual URL ###
        page.goto("https://example.com")  # TODO: update URL

        ### Initialize selector variable ###
        name_field = None

        ### 1. Attempt to locate by ID (preferred) ###
        try:
            name_field = page.locator("#name")
            if not name_field.count():
                raise Exception("Not found")
        except Exception:
            name_field = None

        ### 2. Fallback to locate by Class name ###
        if not name_field:
            try:
                name_field = page.locator(".name-field")
                if not name_field.count():
                    raise Exception("Not found")
            except Exception:
                name_field = None

        ### 3. Fallback to generic CSS selector ###
        if not name_field:
            try:
                name_field = page.locator("input[name='name']")
                if not name_field.count():
                    raise Exception("Not found")
            except Exception:
                name_field = None

        ### 4. Final fallback to XPath expression ###
        if not name_field:
            try:
                name_field = page.locator("//input[@placeholder='Name']")
                if not name_field.count():
                    raise Exception("Not found")
            except Exception:
                name_field = None

        ### Verify that the element was found ###
        if not name_field or not name_field.count():
            raise RuntimeError("Name field could not be located with any selector")

        ### Enter the name 'Alex' into the field ###
        name_field.fill("Alex")

        ### Optional pause to observe the result ###
        page.wait_for_timeout(2000)

        ### Close the browser session ###
        browser.close()

### Run the script when executed directly ###
if __name__ == "__main__":
    run()

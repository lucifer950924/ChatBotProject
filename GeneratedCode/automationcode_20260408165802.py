
### Import necessary modules ###
import asyncio
from playwright.async_api import async_playwright

### Define the main asynchronous function ###
async def run():
    ### Launch Playwright and open a new browser context ###
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for CI
        context = await browser.new_context()
        page = await context.new_page()

        ### Navigate to the target web page (replace with actual URL) ###
        TARGET_URL = "https://example.com"  # <<< UPDATE THIS URL TO THE ACTUAL PAGE >>>
        await page.goto(TARGET_URL)

        ### Try locating the input field by label 'Name' ###
        try:
            name_input = page.get_by_label("Name")
            await name_input.wait_for(state="visible", timeout=5000)
        except Exception:
            ### Fallback: locate by placeholder 'Name' ###
            name_input = page.get_by_placeholder("Name")
            await name_input.wait_for(state="visible", timeout=5000)

        ### Clear any existing text and type 'Alex' into the field ###
        await name_input.fill("")  # Ensure the field is empty
        await name_input.type("Alex")

        ### Verify that the input field now contains the entered value ###
        entered_value = await name_input.input_value()
        assert entered_value == "Alex", f"Expected value 'Alex', but got '{entered_value}'"

        ### Optional: Print success message ###
        print("✅ Input field 'Name' successfully filled with 'Alex' and verified.")

        ### Close browser ###
        await context.close()
        await browser.close()

### Execute the asynchronous function ###
if __name__ == "__main__":
    asyncio.run(run())

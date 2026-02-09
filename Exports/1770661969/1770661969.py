
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Documentation: Set up the browser driver
driver = webdriver.Chrome()  # Replace with your preferred browser

# Documentation: Navigate to Nakri application
driver.get("https://nakri.com")  # Replace with the actual URL of Nakri

try:
    # Documentation: Find and click on the login button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Documentation: Close the browser
    driver.quit()

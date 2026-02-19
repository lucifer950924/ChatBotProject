
# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the browser driver
driver = webdriver.Chrome()

try:
    # Navigate to the RAGAS assessment page
    driver.get("https://example.com/ragas-assessment")

    # Fill out the demographic information form
    driver.find_element_by_name("name").send_keys("John Doe")
    driver.find_element_by_name("age").send_keys("30")
    driver.find_element_by_name("gender").click()

    # Start the RAGAS assessment
    driver.find_element_by_id("start-assessment").click()

    # Loop through each question and select an answer
    for i in range(1, 21):
        question = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//label[{i}]/input"))
        )
        question.click()

    # Submit the assessment
    driver.find_element_by_id("submit-assessment").click()

finally:
    # Close the browser
    driver.quit()

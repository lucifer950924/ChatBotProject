
import pytube
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Set up the browser
driver = webdriver.Chrome()

# Navigate to YouTube
driver.get("https://www.youtube.com/")

# Find the search bar and enter the video title
search_bar = driver.find_element_by_name("search_query")
search_bar.send_keys("Your Video Title")
search_bar.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(2)

# Get the first video result
video_result = driver.find_elements_by_class_name("yt-uix-tile-list-item")[0]

# Click on the video result
video_result.click()

# Wait for the video to start playing
time.sleep(5)

# Close the browser
driver.quit()

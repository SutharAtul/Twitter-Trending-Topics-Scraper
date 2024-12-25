import json
import time
from datetime import datetime
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# X username and password
X_USERNAME = "userkyahai"
X_PASSWORD = "thisismypassword"

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["x_data"]
collection = db["trending_topics"]

# Function to fetch trending topics
def get_trending_topics():
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')

    # Path to ChromeDriver
    service = Service("D:/Project/Stir_Assignments/chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open the login page
        driver.get("https://x.com/i/flow/login")

        # Login process
        username_field = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
        )
        username_field.send_keys(X_USERNAME)
        username_field.send_keys(Keys.RETURN)

        password_field = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
        )
        password_field.send_keys(X_PASSWORD)
        password_field.send_keys(Keys.RETURN)

        # Wait for the trending section
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']//span"))
        )

        # Fetch the trending topics
        trends = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")
        trending_topics = [trend.text for trend in trends[:5]]

        # Record to be stored in MongoDB
        record = {
            "unique_id": str(time.time()),
            "trending_topics": trending_topics,
            "timestamp": datetime.now().isoformat(),  # Use ISO format for consistency
            "ip_address": requests.get('https://api.ipify.org').text
        }

        # Store record in MongoDB
        collection.insert_one(record)

        # Return the record as JSON
        return json.dumps(record)

    except Exception as e:
        print("An error occurred:", e)
        return json.dumps({"error": "Failed to fetch trending topics", "details": str(e)})

    finally:
        driver.quit()

# Main function
if __name__ == "__main__":
    result = get_trending_topics()
    print(result)  # Print result for debugging or logging

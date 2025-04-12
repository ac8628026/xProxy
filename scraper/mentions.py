import os
import time
import re
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

USERNAME = "AshokCh05268450"
CHROME_PROFILE_PATH = r"C:\Users\Ashok choudhary\AppData\Local\Google\Chrome\User Data"
CHROME_PROFILE_NAME = "Profile 12"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    options.add_argument(f"profile-directory={CHROME_PROFILE_NAME}")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def is_logged_in(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/home']"))
        )
        return True
    except:
        return False

def scrape_mentions(driver):
    driver.get("https://x.com/notifications/mentions")
    time.sleep(5)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/status/')]"))
        )
        logging.info(" Mentions page loaded successfully.")
    except:
        logging.warning("Failed to load mentions page.")
        return []

    for i in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    tweets = driver.find_elements(By.XPATH, "//a[contains(@href,'/status/')]")
    tweet_info = []

    for tweet in tweets:
        href = tweet.get_attribute("href")
        match = re.search(r"/status/(\d+)", href)
        if match:
            tweet_info.append({
                "id": match.group(1),
                "href": href
            })

    return tweet_info

def extract_mention_data(driver, mention_ids):
    mention_data = []
    for mention_id in mention_ids:
        try:
            driver.get(f"{mention_id['href']}")
            time.sleep(5)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetText']"))
            )


            tweet_elements = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")

            if len(tweet_elements) >= 2:
                parent_text = tweet_elements[0].text
                mention_text = tweet_elements[1].text
            else:
                parent_text = ""
                mention_text = tweet_elements[0].text if tweet_elements else ""



            timestamp = driver.find_element(By.XPATH, "//time").get_attribute("datetime")


            mention_data.append({
                "id": mention_id['id'],
                "parent_text": parent_text,
                "mention_text": mention_text,
                "timestamp": timestamp,
                "url": mention_id['href']
            })
        except Exception as e:
            logging.error(f"Error fetching content for mention ID {mention_id}: {e}")
            continue

    return mention_data

def login_fun():
    #login login using mail and password
    return False

def get_mentions():
    driver = setup_driver()
    driver.get("https://x.com/home")
    contents = []

    try:
        if is_logged_in(driver):
            logging.info("Logged in and profile loaded.")
            mention_ids = scrape_mentions(driver)
            logging.info(f"Found menthions: {mention_ids}")
            if mention_ids:
                contents = extract_mention_data(driver, mention_ids)
        else:
            logging.warning(" Not logged in. Attempting login fallback.")
            if login_fun():
                logging.info(" Login successful.")
                mention_ids = scrape_mentions(driver)
                if mention_ids:
                    contents = extract_mention_data(driver, mention_ids)
            else:
                logging.warning(" Login failed or not implemented.")
    finally:
        driver.quit()

    return contents

# mentionsdata = mentions()
# print(mentionsdata)
import os
import time
import re
import logging
from dotenv import load_dotenv 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from redisconfig.cache import check_reply

###### "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:\SeleniumProfile" --profile-directory="Default"

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

X_USERNAME = os.getenv("X_USERNAME")
X_PASSWORD = os.getenv("X_PASSWORD")
X_EMAIL = os.getenv("X_EMAIL")

##for customize chrome profile
# CHROME_PROFILE_PATH = r"C:\Users\Ashok choudhary\AppData\Local\Google\Chrome\User Data"
# CHROME_PROFILE_NAME = "Profile 14"

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/SeleniumProfile") 
    options.add_argument("profile-directory=Default") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-notifications")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def is_logged_in(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='/home']"))
        )
        return True
    except:
        return False

def scrape_mentions_ids(driver):
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
    tweet_ids = []
    for tweet in tweets:
        href = tweet.get_attribute("href")
        if "/analytics" in href:
            continue
        match = re.search(r"/status/(\d+)", href)
        if match:
            tweet_ids.append({
                "id": match.group(1),
                "href": href
            })

    return tweet_ids

def extract_mention_data(driver, mention_ids):
    mention_data = []
    for mention_id in mention_ids:
        if check_reply(mention_id["id"]):
            print(f"continue not need : {mention_id}")
            continue
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

def login_fun(driver):
    #login login using email and password
    try:    
        driver.get("https://x.com/i/flow/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))

        #  Enter username
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(X_USERNAME)
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    '//button[@role="button" and .//span[text()="Next"]]'
                ))
            )
            next_button.click()
        except Exception as e:
            logging.error("Could not find the 'Next' button after username input.")
            return False

        time.sleep(2)
        
        page_type = None
        try:
            
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
            )
            page_type = "challenge"
        except:
            page_type = "password"
        if page_type == "challenge":
            WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
            )
            email_field = driver.find_element(By.NAME,"text")
            email_field.send_keys(X_EMAIL)
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        '//button[@role="button" and .//span[text()="Next"]]'
                    ))
                )
                next_button.click()
            except Exception as e:
                logging.error("Could not find the 'Next' button in warning page")
                return False
        elif page_type != "password":
            logging.error("Could not determine the post-username page type.")
            return False
        #  Waiting for password input appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))

        # Enter password
        password_input = driver.find_element(By.NAME, "password")
        
        if not X_PASSWORD:
            logging.error("TWITTER_PASSWORD env variable not set.")
            return False

        password_input.send_keys(X_PASSWORD)
        login_button = driver.find_element(By.XPATH, '//button[@role="button" and .//span[text()="Log in"]]')
        login_button.click()

        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@href='/home']")))

        logging.info("Login successful.")
        return True

    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False
    

def get_mentions():
    driver = setup_driver()
    #print("driver setup successfully")
    driver.get("https://x.com/home")
    #print("home page loaded")
    contents = []

    try:
        if is_logged_in(driver):
            logging.info("Logged in and profile loaded.")
            mention_ids = scrape_mentions_ids(driver)
            # #print(f"mention ids {mention_ids}")
            if mention_ids:
                contents = extract_mention_data(driver, mention_ids)
                # #print(f"contents {contents}")
        else:
            logging.warning(" Not logged in. Attempting login fallback.")
            if login_fun(driver):
                logging.info(" Login successful.")
                mention_ids = scrape_mentions_ids(driver)
               
                if mention_ids:
                    contents = extract_mention_data(driver, mention_ids)
                    
            else:
                logging.warning(" Login failed or not implemented.")
    finally:
        driver.quit()

    return contents

# mentionsdata = get_mentions()
# #print(mentionsdata)
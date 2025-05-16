import tweepy
import os
from dotenv import load_dotenv 
import logging



# Set up logging configuration
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

load_dotenv()




def create_twitter_client():
    client = tweepy.Client(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )
    return client

def reply_to_tweet(tweet_id ,reply_text):
   
    
    client = create_twitter_client()

    try:
        response = client.create_tweet(
            text=reply_text,
            in_reply_to_tweet_id=tweet_id
        )
      #   logging.info(f"Replied to tweet ID {tweet_id} with: {reply_text}")

        return response
    except Exception as e:
        logging.error(f"Error replying to tweet ID {tweet_id}: {e}")
        return False
    

# reply = reply_to_tweet(tweet_id=1910778685977673840, reply_text="will akch get back to you?")

# print(reply)
from fastapi import FastAPI
from scraper.mentions import get_mentions



app = FastAPI()


@app.get("/")
def scrape_mentions():
    mentions = get_mentions()
    return mentions
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from x_bot import x_bot

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot is running!"}

@app.on_event("startup")
@repeat_every(seconds=120) 
def run_x_bot_background_task() -> None:
    x_bot()

from fastapi import FastAPI
import asyncio
import logging
from contextlib import asynccontextmanager
from x_bot import x_bot

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Store background tasks
background_tasks = set()

# run the bot 
async def run_bot_with_error_handling():
    try:
        logger.info("Running X bot task")
        x_bot()
       
    except Exception as e:
        logger.error(f"Error running X bot: {str(e)}")

# Background task runs every 30 seconds
async def scheduled_task():
    while True:
        await run_bot_with_error_handling()
        await asyncio.sleep(30)  

# Registering the background task
async def start_background_tasks():
    task = asyncio.create_task(scheduled_task())
    background_tasks.add(task) # add task 
    task.add_done_callback(background_tasks.remove) #remove task when done

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background task with app starts
    await start_background_tasks()
    yield
    

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "Bot is running!"}
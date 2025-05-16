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

# Function to run the bot and handle errors
async def run_bot_with_error_handling():
    try:
        logger.info("Running X bot task")
        # If x_bot is synchronous
        x_bot()
        # If x_bot is asynchronous, use:
        # await x_bot()
    except Exception as e:
        logger.error(f"Error running X bot: {str(e)}")

# Background task that runs every 2 minutes
async def scheduled_task():
    while True:
        await run_bot_with_error_handling()
        await asyncio.sleep(30)  # 2 minutes

# Register the background task
async def start_background_tasks():
    task = asyncio.create_task(scheduled_task())
    # Add task to the set to prevent it from being garbage collected
    background_tasks.add(task)
    # Remove task from set when it's done
    task.add_done_callback(background_tasks.remove)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background task when the app starts
    await start_background_tasks()
    yield
    # Could add cleanup code here if needed

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"status": "Bot is running!"}
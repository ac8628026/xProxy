import redis
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_redis_client():
    try:
        redis_client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
        
        if redis_client.ping():
            return redis_client
        
    except Exception as e:
        logging.error("Could not connect to Redis. Error: {e}")
        return None









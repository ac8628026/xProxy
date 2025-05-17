from .redis_client import get_redis_client

def mark_as_replyed(mention_id):
    client = get_redis_client()
    if client:
        client.set(f"replied:{mention_id}", "1")
        # print(f"Added {mention_id} in Redis")

def check_reply(mention_id):
    client = get_redis_client()
    if client:
        return client.exists(f"replied:{mention_id}") == 1
    return False 

def mark_as_unreplyed(mention_id):
    client = get_redis_client()
    if client:
        client.delete(f"replied:{mention_id}")

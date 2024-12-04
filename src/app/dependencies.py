from redis import Redis
from src.app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

def get_cached_response(key):
    return redis_client.get(key)

def set_cached_response(key, value, expiration=3600):
    redis_client.set(key, value, ex=expiration)

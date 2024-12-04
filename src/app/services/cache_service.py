from src.app.dependencies import redis_client

def get_cached_data(key):
    data = redis_client.get(key)
    return eval(data) if data else None

def set_cached_data(key, data, ttl=3600):
    redis_client.setex(key, ttl, str(data))

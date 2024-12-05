import redis

try:
    redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    redis_client.ping()
    print("Successfully connected to Redis!")
except redis.ConnectionError as e:
    print(f"Failed to connect to Redis: {e}")

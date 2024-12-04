from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration settings
API_KEY = os.getenv("API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

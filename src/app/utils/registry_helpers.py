import os
import requests

REGISTRY_URL = os.getenv("SERVICE_REGISTRY_URL", "http://localhost:4471")
SERVICE_NAME = os.getenv("SERVICE_NAME", "market-news-service")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8000")
JWT_SECRET = os.getenv("JWT_SECRET", "CS4471")

jwt_token = None

def authenticate():
    """Authenticate with the service registry to obtain a JWT token."""
    global jwt_token
    try:
        response = requests.post(
            f"{REGISTRY_URL}/login",
            json={"username": os.getenv("ADMIN_USER"), "password": os.getenv("ADMIN_PASS")}
        )
        response.raise_for_status()
        jwt_token = response.json().get("accessToken")
        print("Authenticated successfully!")
    except Exception as e:
        print(f"Error during authentication: {e}")
        raise

def register_service():
    """Register the microservice with the service registry."""
    try:
        response = requests.post(
            f"{REGISTRY_URL}/register",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={
                "serviceName": SERVICE_NAME,
                "port": SERVICE_PORT,
                "description": "Market News Sentiment Microservice",
                "version": "1.0.0",
                "instanceId": os.getenv("INSTANCE_ID", "1"),
                "url": f"http://localhost:{SERVICE_PORT}"
            }
        )
        response.raise_for_status()
        print("Service registered successfully!")
    except Exception as e:
        print(f"Error registering service: {e}")
        raise

def deregister_service():
    """Deregister the microservice from the service registry."""
    try:
        response = requests.post(
            f"{REGISTRY_URL}/deregister",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={"serviceName": SERVICE_NAME, "instanceId": os.getenv("INSTANCE_ID", "1")}
        )
        response.raise_for_status()
        print("Service deregistered successfully!")
    except Exception as e:
        print(f"Error deregistering service: {e}")
        raise

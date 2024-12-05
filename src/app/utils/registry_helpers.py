import os
import requests
import threading
import time

# Environment variables
REGISTRY_URL = os.getenv("SERVICE_REGISTRY_ADDRESS", "http://localhost:4471")
SERVICE_NAME = os.getenv("SERVICE_NAME", "market-news-service")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8000")
INSTANCE_ID = os.getenv("INSTANCE_ID", "1")
jwt_token = None

def authenticate():
    """Authenticate with the service registry to obtain a JWT token."""
    global jwt_token
    try:
        response = requests.post(
            f"{REGISTRY_URL}/login",
            json={
                "username": os.getenv("ADMIN_USER"),
                "password": os.getenv("ADMIN_PASS"),
            },
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
                "instanceId": INSTANCE_ID,
                "url": f"http://localhost:{SERVICE_PORT}",
            },
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
            json={"serviceName": SERVICE_NAME, "instanceId": INSTANCE_ID},
        )
        response.raise_for_status()
        print("Service deregistered successfully!")
    except Exception as e:
        print(f"Error deregistering service: {e}")
        raise

def send_heartbeat():
    """Send periodic heartbeats by re-registering the service."""
    while True:
        try:
            response = requests.post(
                f"{REGISTRY_URL}/reregister",
                headers={"Authorization": f"Bearer {jwt_token}"},
                json={
                    "serviceName": SERVICE_NAME,
                    "instanceId": INSTANCE_ID,
                },
            )
            if response.status_code == 200:
                print(f"Heartbeat sent for {SERVICE_NAME}: {response.json()}")
            else:
                print(f"Heartbeat failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending heartbeat: {e}")
        time.sleep(10)  # Send heartbeat every 10 seconds

def start_heartbeat_thread():
    """Start the heartbeat thread."""
    heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
    heartbeat_thread.start()

import requests
from src.app.config import API_KEY

def fetch_news_from_api(tickers: str, start_date: str = None, end_date: str = None, topics: str = None, sort: str = "LATEST", limit: int = 50):
    """Fetch news from Alpha Vantage API."""
    BASE_URL = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",  # Include the function parameter explicitly
        "tickers": tickers,
        "apikey": API_KEY,
        "sort": sort,
        "limit": limit
    }

    if start_date:
        params["time_from"] = start_date.replace("-", "") + "T0000"
    if end_date:
        params["time_to"] = end_date.replace("-", "") + "T2359"
    if topics:
        params["topics"] = topics

    print(f"Making request to Alpha Vantage with params: {params}")

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()

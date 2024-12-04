from src.app.utils.api_helpers import fetch_news_from_api

def filter_news_data(raw_data):
    """Filter relevant fields from API response."""
    if not raw_data or "feed" not in raw_data:
        return {"message": "No news data found."}

    filtered_news = []
    for article in raw_data.get("feed", []):
        print("Processing Article:", article)  # Debug individual articles
        filtered_news.append({
            "headline": article.get("title"),
            "summary": article.get("summary"),
            "source": article.get("source"),
            "published_at": article.get("time_published"),
        })
    return filtered_news


from fastapi import APIRouter, HTTPException, Query
from src.app.services.news_service import fetch_news_from_api, filter_news_data
from src.app.dependencies import get_cached_response, set_cached_response
import json

router = APIRouter()

@router.get("/news")
async def get_news(
    tickers: str = Query(..., description="Company ticker symbols (e.g., MSFT, AAPL)"),
    start_date: str = Query(None, description="Start date for news (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date for news (YYYY-MM-DD)"),
    topics: str = Query(None, description="News topics to filter by (e.g., ipo,technology)"),
    sort: str = Query("LATEST", description="Sort order (LATEST, EARLIEST, RELEVANCE)"),
    limit: int = Query(50, description="Number of articles to retrieve (default: 50)")
):
    """
    Endpoint to fetch market news and sentiment for a company.
    """
    try:
        # Create cache key
        cache_key = f"{tickers}:{start_date}:{end_date}:{topics}:{sort}:{limit}"
        cached_data = get_cached_response(cache_key)
        if cached_data:
            return {"status": "success", "data": json.loads(cached_data)}

        # Fetch news from API
        raw_news = fetch_news_from_api(tickers, start_date, end_date, topics, sort, limit)
        filtered_news = filter_news_data(raw_news)

        # Cache the result
        set_cached_response(cache_key, json.dumps(filtered_news))

        return {"status": "success", "data": filtered_news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

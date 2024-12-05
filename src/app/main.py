from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.app.routes.news_routes import router as news_router
from src.app.utils.registry_helpers import (
    authenticate,
    register_service,
    deregister_service,
    start_heartbeat_thread,
)
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins --> replace with specific URLs in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include routes
app.include_router(news_router, prefix="/api", tags=["News"])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>News Sentiment Service</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }
                .container {
                    max-width: 800px;
                    margin: auto;
                }
                input, select, button {
                    display: block;
                    width: 100%;
                    margin: 10px 0;
                    padding: 10px;
                    font-size: 16px;
                }
                .news-item {
                    border: 1px solid #ccc;
                    padding: 10px;
                    margin-bottom: 10px;
                    background-color: #f9f9f9;
                }
                .news-item h2 {
                    font-size: 18px;
                    margin: 0 0 5px;
                }
                .news-item p {
                    margin: 5px 0;
                }
                .news-item .source {
                    font-weight: bold;
                }
                .news-item .published_at {
                    font-size: 14px;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>News Sentiment Service</h1>
                <form id="newsForm">
                    <label for="tickers">Ticker Symbols (comma-separated):</label>
                    <input type="text" id="tickers" name="tickers" placeholder="e.g., MSFT, AAPL" required>

                    <label for="start_date">Start Date (YYYY-MM-DD):</label>
                    <input type="date" id="start_date" name="start_date">

                    <label for="end_date">End Date (YYYY-MM-DD):</label>
                    <input type="date" id="end_date" name="end_date">

                    <label for="topics">Topics (comma-separated):</label>
                    <input type="text" id="topics" name="topics" placeholder="e.g., technology,ipo">

                    <label for="sort">Sort Order:</label>
                    <select id="sort" name="sort">
                        <option value="LATEST">Latest</option>
                        <option value="EARLIEST">Earliest</option>
                        <option value="RELEVANCE">Relevance</option>
                    </select>

                    <label for="limit">Number of Articles:</label>
                    <input type="number" id="limit" name="limit" value="50" min="1">

                    <button type="button" onclick="fetchNews()">Get News</button>
                </form>

                <div id="newsContainer"></div>
            </div>

            <script>
                async function fetchNews() {
                    const tickers = document.getElementById("tickers").value;
                    const start_date = document.getElementById("start_date").value;
                    const end_date = document.getElementById("end_date").value;
                    const topics = document.getElementById("topics").value;
                    const sort = document.getElementById("sort").value;
                    const limit = document.getElementById("limit").value;

                    let apiUrl = `http://127.0.0.1:8000/api/news?tickers=${tickers}&sort=${sort}&limit=${limit}`;
                    
                    if (start_date) {
                        apiUrl += `&start_date=${start_date}`;
                    }
                    if (end_date) {
                        apiUrl += `&end_date=${end_date}`;
                    }
                    if (topics) {
                        apiUrl += `&topics=${topics}`;
                    }

                    try {
                        const response = await fetch(apiUrl);
                        const data = await response.json();
                        displayNews(data.data);
                    } catch (error) {
                        document.getElementById("newsContainer").textContent = `Error: ${error.message}`;
                    }
                }

                function displayNews(newsData) {
                    const newsContainer = document.getElementById("newsContainer");
                    newsContainer.innerHTML = "";

                    if (newsData && newsData.length > 0) {
                        newsData.forEach(article => {
                            const newsItem = document.createElement("div");
                            newsItem.className = "news-item";

                            const headline = document.createElement("h2");
                            headline.textContent = article.headline;
                            newsItem.appendChild(headline);

                            const summary = document.createElement("p");
                            summary.textContent = article.summary;
                            newsItem.appendChild(summary);

                            const source = document.createElement("p");
                            source.className = "source";
                            source.textContent = `Source: ${article.source}`;
                            newsItem.appendChild(source);

                            const publishedAt = document.createElement("p");
                            publishedAt.className = "published_at";
                            publishedAt.textContent = `Published At: ${formatDate(article.published_at)}`;
                            newsItem.appendChild(publishedAt);

                            newsContainer.appendChild(newsItem);
                        });
                    } else {
                        newsContainer.textContent = "No news data found.";
                    }
                }

                function formatDate(dateString) {
                    const year = dateString.substring(0, 4);
                    const month = dateString.substring(4, 6);
                    const day = dateString.substring(6, 8);
                    const hour = dateString.substring(9, 11);
                    const minute = dateString.substring(11, 13);
                    return `${year}-${month}-${day} ${hour}:${minute}`;
                }
            </script>
        </body>
        </html>
"""

# Path to the frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))


# Register the service and start the heartbeat on application startup
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    authenticate()
    register_service()
    start_heartbeat_thread()

# Deregister the service on application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    deregister_service()

import json
import time
import requests
from datetime import datetime

# Configuration
GNEWS_API_KEY = "74031bf7824c47afe049ba5835d4469470086"  # Replace with your GNews API key
CATEGORIES = ["general", "nation", "world", "business", "technology", "entertainment", "sports", "science", "health"]
INTERVAL = 1800  # Fetch news every 30 minutes
BASE_URL = "https://gnews.io/api/v4/top-headlines?category={}&apikey={}&lang=en"

def fetch_news(category):
    """Fetches news articles from the GNews API for a given category."""
    response = requests.get(BASE_URL.format(category, GNEWS_API_KEY))
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print(f"Failed to fetch news for {category}. Status Code: {response.status_code}")
        return []

def load_existing_news():
    """Loads existing news data from separate JSON files."""
    news_data = {}
    for category in CATEGORIES:
        try:
            with open(f"{category}_news.json", "r") as file:
                news_data[category] = json.load(file).get(category, [])
        except (FileNotFoundError, json.JSONDecodeError):
            news_data[category] = []
    return news_data

def save_news(news_data):
    """Saves news data to separate JSON files per category."""
    for category, articles in news_data.items():
        with open(f"{category}_news.json", "w") as file:
            json.dump({category: articles}, file, indent=2)

def update_news():
    """Fetches latest news for each category and updates the JSON files without duplicates."""
    existing_news = load_existing_news()

    for category in CATEGORIES:
        new_articles = fetch_news(category)
        existing_articles = existing_news.get(category, [])
        existing_urls = {article["url"] for article in existing_articles}

        for article in new_articles:
            if article["url"] not in existing_urls:
                formatted_article = {
                    "source": {
                        "id": article.get("source", {}).get("id", "dummy-id"),
                        "name": article.get("source", {}).get("name", "Unknown Source")
                    },
                    "author": article.get("author", "Unknown Author"),
                    "title": article.get("title", "No Title"),
                    "description": article.get("description", "No Description"),
                    "url": article.get("url", ""),
                    "urlToImage": article.get("image", ""),
                    "publishedAt": article.get("publishedAt", datetime.utcnow().isoformat()),
                    "content": article.get("content", "No Content")
                }
                existing_articles.append(formatted_article)

        existing_news[category] = existing_articles

    save_news(existing_news)
    print(f"Updated news at {datetime.utcnow().isoformat()}")

if __name__ == "__main__":
    while True:
        update_news()
        time.sleep(INTERVAL)

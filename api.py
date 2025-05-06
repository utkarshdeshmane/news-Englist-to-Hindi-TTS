import requests
import urllib.parse 

API_KEY = "b133a9477b9645729e0908fc27f18092"


def fetch_news(query):
    query = urllib.parse.quote(query)  # Encode query properly
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}&language=en&pageSize=5"

    try:
        response = requests.get(url, timeout=10)  # Add timeout for API request

        if response.status_code != 200:
            print(f"Error: News API returned {response.status_code}")
            return []

        data = response.json()
        seen_titles = set()  # To remove duplicates

        articles = []
        for article in data.get("articles", []):
            title = article.get("title", "").strip()
            summary = article.get("description", "").strip() or title  # Use title if summary missing
            url = article.get("url", "")

            if title and summary and title not in seen_titles:
                seen_titles.add(title)
                articles.append({"title": title, "url": url, "summary": summary})

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

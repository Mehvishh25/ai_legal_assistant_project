from flask import Blueprint, render_template
import requests

news_bp = Blueprint("news", __name__, template_folder="../templates")

# ✅ Your working NewsAPI key
NEWS_API_KEY = "510a34343fbb4c04bdf0d9fd1bb24a43"  # replace with your actual key

@news_bp.route('/legal-news')
def legal_news():
    url = "https://newsapi.org/v2/everything"

    params = {
        'q': 'law OR legal OR supreme court OR court case OR litigation OR bar council OR PIL OR judge',
        'language': 'en',
        'sortBy': 'publishedAt',
        'pageSize': 10,
        'apiKey': NEWS_API_KEY  # ✅ Correct way to pass API key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        if not articles:
            print("⚠️ No articles received")
        return render_template("legal-news.html", articles=articles)
    except Exception as e:
        print("❌ Error fetching news:", e)
        return f"Error fetching news: {str(e)}", 500

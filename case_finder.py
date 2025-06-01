# case_finder.py

from flask import Blueprint, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
import re

case_finder_bp = Blueprint('case_finder', __name__)
load_dotenv()

# Configure Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def google_search_urls(query, max_results=3):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    search_url = f"https://www.google.com/search?q=site:indiankanoon.org+{query.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)

    # Save raw HTML for debugging
    with open("google_debug.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    soup = BeautifulSoup(response.text, "html.parser")
    urls = []

    for a in soup.select("a[href^='http']"):
        href = a["href"]
        if "indiankanoon.org/doc/" in href:
            match = re.search(r"https://www\.indiankanoon\.org/doc/\d+/?", href)
            if match:
                url = match.group(0)
                if url not in urls:
                    urls.append(url)
        if len(urls) >= max_results:
            break

    print("✅ Extracted URLs:", urls)
    return urls

def fetch_case_content(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        title_tag = soup.find("h1")
        content_div = soup.find("div", class_="doc_content") or soup.find("pre")
        text = content_div.get_text(separator="\n").strip() if content_div else ""

        return {
            "title": title_tag.get_text(strip=True) if title_tag else "Unknown Title",
            "url": url,
            "text": text[:10000]  # Limit to 10k characters for Gemini input
        }
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

def build_prompt(query, case_data_list):
    context_blocks = "\n\n".join([
        f"---\nTitle: {case['title']}\nURL: {case['url']}\nContent:\n{case['text']}"
        for case in case_data_list
    ])

    prompt = f"""
You are a legal assistant. Given the user's query: "{query}", analyze the following Indian case documents and extract the most relevant cases.

For each relevant case, return a JSON object with:
- "title"
- "citation" (if mentioned)
- "date" (if mentioned)
- "summary" (max 200 words)
- "articles" (related constitutional articles)
- "url"
- "preview" (excerpt from the case)

Format the output as a JSON array of up to 3 cases. No explanation, no markdown. Just valid JSON.

Here is the data:

{context_blocks}
"""
    return prompt.strip()

@case_finder_bp.route('/find-cases', methods=['POST'])
def find_cases():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query required"}), 400

    try:
        urls = google_search_urls(query)
        if not urls:
            print("❌ No case URLs found in Google search.")
            return jsonify([])

        case_data = []
        for url in urls:
            content = fetch_case_content(url)
            if content:
                case_data.append(content)

        if not case_data:
            print("❌ No usable case content scraped.")
            return jsonify([])

        prompt = build_prompt(query, case_data)
        response = model.generate_content(prompt)

        raw_output = response.text.strip()
        cleaned = raw_output.removeprefix("```json").removesuffix("```").strip()

        import json
        result = json.loads(cleaned)
        print("✅ Gemini returned:", result)
        return jsonify(result)

    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return jsonify({"error": str(e)}), 500

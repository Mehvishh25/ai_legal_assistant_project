# chatbot.py

import os
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# ---------------- ENV ---------------- #

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# ---------------- Blueprint ---------------- #

chatbot_bp = Blueprint("chatbot", __name__)

# ---------------- LLM ---------------- #

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_retries=3,
)

# ---------------- Route ---------------- #

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question is required."}), 400

        prompt = f"""
You are a helpful legal assistant.
Answer clearly, simply, and professionally.

Question:
{question}
"""

        response = llm.invoke([
            HumanMessage(content=prompt)
        ])

        return jsonify({
            "answer": response.content.strip()
        })

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

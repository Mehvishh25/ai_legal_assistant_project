# chatbot.py
import os
from flask import Blueprint, request, jsonify
from google.generativeai import configure, GenerativeModel

chatbot_bp = Blueprint('chatbot', __name__)

# Configure Gemini with API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
configure(api_key=GOOGLE_API_KEY)

# Load model once
model = GenerativeModel('gemini-1.5-flash')

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "Question is required."}), 400

        prompt = f"You are a helpful legal assistant. Answer the following question in clear and simple terms:\n\n{question}\n\nAnswer:"
        response = model.generate_content(prompt)

        return jsonify({"answer": response.text.strip()})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

# chatbot.py
from flask import Blueprint, request, jsonify
from huggingface_hub import InferenceClient
import os

chatbot_bp = Blueprint('chatbot', __name__)
HF_API_KEY = os.getenv("HF_API_KEY")

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    model_name = data.get("model", "mistralai/Mixtral-8x7B-Instruct-v0.1")

    if not question:
        return jsonify({"error": "Question is required."}), 400

    client = InferenceClient(model=model_name, token=HF_API_KEY)
    prompt = f"You are a helpful legal assistant. Answer this in simple terms:\n\n{question}"
    response = client.text_generation(prompt, max_new_tokens=300, temperature=0.2)

    return jsonify({"answer": response.strip()})

# pdf_qa.py
from flask import Blueprint, request, jsonify
from huggingface_hub import InferenceClient
import os

pdfqa_bp = Blueprint('pdfqa', __name__)
HF_API_KEY = os.getenv("HF_API_KEY")

@pdfqa_bp.route('/pdf-qa', methods=['POST'])
def pdf_qa():
    data = request.get_json()
    question = data.get("question", "")
    model_name = data.get("model", "tiiuae/falcon-7b-instruct")

    if not question:
        return jsonify({"error": "Question is required."}), 400

    client = InferenceClient(model=model_name, token=HF_API_KEY)
    prompt = f"Answer based on legal document context:\n\n{question}"
    response = client.text_generation(prompt, max_new_tokens=300, temperature=0.2)

    return jsonify({"answer": response.strip()})

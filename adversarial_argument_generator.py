# adversarial_argument_generator.py
from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os

adversary_bp = Blueprint('adversarial_argument', __name__)

# Configure Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@adversary_bp.route("/adversarial-arguments", methods=["POST"])
def generate_arguments():
    data = request.get_json()
    case_description = data.get("case")

    if not case_description:
        return jsonify({"error": "Missing case description."}), 400

    prompt = f"""
    You are a legal expert. Given the case description below, generate:
    1. An argument supporting the prosecution or petitioner.
    2. A counter-argument from the defense or respondent.
    Cite any relevant laws or precedents if applicable.

    Case: {case_description}

    Format:
    - Prosecution Argument:
    - Defense Argument:
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"arguments": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

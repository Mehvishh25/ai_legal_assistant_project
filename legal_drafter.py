# legal_drafter.py
from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os

drafter_bp = Blueprint('drafter', __name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@drafter_bp.route('/draft', methods=['POST'])
def draft():
    data = request.get_json()
    doc_type = data.get("type")
    inputs = data.get("inputs")

    if not doc_type or not inputs:
        return jsonify({"error": "Document type and inputs are required."}), 400

    prompt = get_prompt(doc_type, inputs)
    response = model.generate_content(prompt)

    return jsonify({"document": response.text})

def get_prompt(doc_type, inputs):
    if doc_type == "nda":
        return f"Draft NDA between {inputs['party_a']} and {inputs['party_b']} for {inputs['purpose']} valid for {inputs['duration']}."
    elif doc_type == "lease":
        return f"Draft Lease Agreement: Landlord {inputs['landlord']}, Tenant {inputs['tenant']}, Address: {inputs['address']}, Term: {inputs['term']}, Rent: {inputs['rent']}."
    elif doc_type == "will":
        return f"Draft Will: Name {inputs['name']}, Beneficiaries: {inputs['beneficiaries']}, Executor: {inputs['executor']}."
    elif doc_type == "contract":
        return f"Draft Contract between {inputs['party_a']} and {inputs['party_b']} for {inputs['purpose']} lasting {inputs['duration']}, Payment: {inputs['payment_terms']}."
    else:
        return "Invalid document type."

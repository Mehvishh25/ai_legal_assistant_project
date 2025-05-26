# summary.py
from flask import Blueprint, request, jsonify
from pypdf import PdfReader
from pdf2image import convert_from_bytes
import pytesseract
from langdetect import detect
import re

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/summarize', methods=['POST'])
def summarize():
    file = request.files.get('file')
    input_text = request.form.get('text', '')
    summary_length = request.form.get('length', 'medium')

    if not file and not input_text:
        return jsonify({"error": "No input provided."}), 400

    text = ""

    if file:
        if file.filename.endswith('.pdf'):
            pdf = PdfReader(file)
            for page in pdf.pages:
                content = page.extract_text()
                if content and detect_lang(content):
                    text += content
            if not text:
                images = convert_from_bytes(file.read())
                for img in images:
                    text += pytesseract.image_to_string(img)
        elif file.filename.endswith('.txt'):
            text = file.read().decode('utf-8')

    if input_text:
        text += input_text.strip()

    chunks = chunk_text(text)
    summarized_text = summarize_chunks(chunks)

    keywords = ["termination", "liability", "jurisdiction", "confidentiality", "indemnity", "governing law", "dispute", "arbitration", "payment", "intellectual property"]
    clauses = extract_clauses(text, keywords)

    return jsonify({
        "summary": summarized_text,
        "clauses": clauses
    })

def chunk_text(text, chunk_size=1000):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_chunks(chunks):
    return " ".join([". ".join(chunk.split(". ")[:3]) + "." for chunk in chunks])

def detect_lang(text):
    try:
        return detect(text) == 'en'
    except:
        return False

def extract_clauses(text, keywords):
    clauses = {kw: [] for kw in keywords}
    sentences = re.split(r'(?<=[.!?]) +', text)
    for sentence in sentences:
        for kw in keywords:
            if kw in sentence.lower():
                clauses[kw].append(sentence.strip())
    return {k: v for k, v in clauses.items() if v}

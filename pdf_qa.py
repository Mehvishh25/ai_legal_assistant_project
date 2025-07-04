import os
import tempfile
import traceback
from flask import Blueprint, request, jsonify
import fitz  # PyMuPDF
from google.generativeai import configure, GenerativeModel
from langdetect import detect

pdfqa_bp = Blueprint('pdfqa_bp', __name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
configure(api_key=GOOGLE_API_KEY)

model = GenerativeModel('gemini-1.5-flash')

# 🧠 In-memory temporary chat history (resets every server restart)
chat_history = []

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for i, page in enumerate(doc):
                page_text = page.get_text()
                text += f"\n--- Page {i+1} ---\n{page_text.strip()}"
    except Exception as e:
        text += f"\n[Text extraction failed: {str(e)}]"
    return text

@pdfqa_bp.route("/api/pdf-qa", methods=["POST"])
def pdf_qa():
    try:
        file = request.files.get("file")
        question = request.form.get("question", "").strip()

        if not file or not question:
            return jsonify({"error": "File and question are required"}), 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            file.save(tmp_pdf.name)
            extracted_text = extract_text_from_pdf(tmp_pdf.name)

        try:
            lang = detect(question)
        except:
            lang = "en"

        prompt = f"""You are a legal assistant AI. Based on the following document content, answer the user's question.

Document Content:
\"\"\"
{extracted_text[:20000]}
\"\"\"

Question: {question}
Answer:"""

        response = model.generate_content(prompt)
        answer = response.text.strip()

        # ⏳ Store in chat history
        chat_history.append({"question": question, "answer": answer})

        return jsonify({
            "answer": answer,
            "history": chat_history  # Send full temporary session
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

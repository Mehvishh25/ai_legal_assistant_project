import os
import tempfile
import traceback

from flask import Blueprint, request, jsonify
from pypdf import PdfReader
from langdetect import detect
from dotenv import load_dotenv

# LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ------------------------------
# Load ENV
# ------------------------------
load_dotenv()

pdfqa_bp = Blueprint('pdfqa_bp', __name__)

# ------------------------------
# LLM (LangChain Gemini)
# ------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3,
    max_retries=3,
    timeout=60
)

# ------------------------------
# Prompt Template
# ------------------------------
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a legal assistant AI. Answer strictly based on provided document."),
    ("human", "{input}")
])

chain = prompt_template | llm | StrOutputParser()

# ------------------------------
# TEXT EXTRACTION USING PYPDF
# ------------------------------
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)

    for i, page in enumerate(reader.pages):
        try:
            page_text = page.extract_text() or ""
            text += f"\n--- Page {i+1} ---\n{page_text.strip()}"
        except Exception as e:
            text += f"\n--- Page {i+1} ---\n[Text Extraction Failed: {str(e)}]"

    return text


# ------------------------------
# API Endpoint
# ------------------------------
@pdfqa_bp.route("/api/pdf-qa", methods=["POST"])
def pdf_qa():
    try:
        file = request.files.get("file")
        question = request.form.get("question", "").strip()

        if not file or not question:
            return jsonify({"error": "File and question are required"}), 400

        # Save temp PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            file.save(tmp_pdf.name)
            extracted_text = extract_text_from_pdf(tmp_pdf.name)

        # Language detection (optional)
        try:
            lang = detect(question)
        except:
            lang = "en"

        final_prompt = f"""You are a legal assistant AI. Based on the following document content, answer the user's question.

Document Content:
\"\"\"
{extracted_text[:20000]}
\"\"\"

Question: {question}
Answer:"""

        answer = chain.invoke({
            "input": final_prompt
        })

        return jsonify({"answer": answer})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500

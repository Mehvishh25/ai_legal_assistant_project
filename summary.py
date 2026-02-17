from flask import Blueprint, request, jsonify
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

# LangChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ------------------------------
# Load ENV
# ------------------------------
load_dotenv()

summary_bp = Blueprint("summary", __name__)

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
    ("system", "You are a legal assistant. Summarize legal documents in simple language and extract key clauses."),
    ("human", "{input}")
])

chain = prompt_template | llm | StrOutputParser()

# ------------------------------
# API
# ------------------------------
@summary_bp.route("/summarize", methods=["POST"])
def summarize_pdf():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    # ------------------------------
    # Extract PDF Text (UNCHANGED)
    # ------------------------------
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
    except Exception as e:
        return jsonify({"error": "Failed to read PDF"}), 500

    # ------------------------------
    # Prompt (Same Logic)
    # ------------------------------
    final_prompt = f"""
You are a legal assistant. Summarize the following legal document in simple language.
Also, extract any important clauses or sections, and return them separately.

Document:
{text[:10000]}
"""

    try:
        output = chain.invoke({
            "input": final_prompt
        })

        # ------------------------------
        # SAME Parsing Logic
        # ------------------------------
        if "Important Clauses" in output:
            summary_text, clauses = output.split("Important Clauses", 1)
            clauses_lines = clauses.strip().split("\n")
            clause_dict = {}

            for line in clauses_lines:
                if ":" in line:
                    key, val = line.split(":", 1)
                    clause_dict[key.strip()] = [v.strip() for v in val.split(";")]

        else:
            summary_text = output
            clause_dict = {}

        return jsonify({
            "summary": summary_text.strip(),
            "clauses": clause_dict
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load ENV
load_dotenv()

adversary_bp = Blueprint('adversarial_argument', __name__)

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a legal expert generating strong courtroom arguments."),
    ("human", """
Given the case description below, generate:

1. Prosecution / Petitioner Argument
2. Defense / Respondent Counter Argument
Include relevant laws or precedents if applicable.

Case:
{case_description}

Format:
- Prosecution Argument:
- Defense Argument:
""")
])

# Chain (NEW STYLE)
chain = prompt | llm | StrOutputParser()


@adversary_bp.route("/adversarial-arguments", methods=["POST"])
def generate_arguments():
    try:
        data = request.get_json()
        case_description = data.get("case", "").strip()

        if not case_description:
            return jsonify({"error": "Missing case description"}), 400

        result = chain.invoke({
            "case_description": case_description
        })

        return jsonify({"arguments": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

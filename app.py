from flask import Flask, render_template
from dotenv import load_dotenv
from summary import summary_bp
from chatbot import chatbot_bp
from pdf_qa import pdfqa_bp
from legal_drafter import drafter_bp
from case_finder import case_finder_bp  # ✅ NEW
import os

# Load environment variables from .env
load_dotenv()

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Register blueprints
app.register_blueprint(summary_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(pdfqa_bp)
app.register_blueprint(drafter_bp)
app.register_blueprint(case_finder_bp)  # ✅ NEW

# Routes for frontend pages
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/blog')
def blog():
    return render_template("blog.html")

@app.route('/pdf-summary')
def pdf_summary():
    return render_template("pdf-summary.html")

@app.route('/pdf-qa')
def pdf_qa():
    return render_template("pdf-qa.html")

@app.route('/legal-chat')
def legal_chat():
    return render_template("legal-chat.html")

@app.route('/legal-doc-drafter')
def legal_doc_drafter():
    return render_template("legal-doc-drafter.html")

@app.route('/case-finder')  # ✅ NEW ROUTE
def case_finder():
    return render_template("legal-case-finder.html")

@app.route('/health')
def health():
    return "✅ Server is running", 200

# Run the app
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)

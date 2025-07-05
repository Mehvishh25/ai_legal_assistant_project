# app.py
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os

# Blueprints
from summary import summary_bp
from chatbot import chatbot_bp
from pdf_qa import pdfqa_bp
from legal_drafter import drafter_bp
from case_finder import case_finder_bp
from adversarial_argument_generator import adversary_bp
from news import news_bp
from bot_webhook import bot_bp  # Webhook-based Telegram bot

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

# Register blueprints
app.register_blueprint(summary_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(pdfqa_bp)
app.register_blueprint(drafter_bp)
app.register_blueprint(case_finder_bp)
app.register_blueprint(adversary_bp)
app.register_blueprint(news_bp)
app.register_blueprint(bot_bp)

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

@app.route('/case-finder')
def case_finder():
    return render_template("legal-case-finder.html")

@app.route('/adversarial-generator')
def adversarial_generator():
    return render_template("adversarial-generator.html")

@app.route('/health')
def health():
    return "✅ Server is running", 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

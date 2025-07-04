# app.py
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from summary import summary_bp
from chatbot import chatbot_bp
from pdf_qa import pdfqa_bp
from legal_drafter import drafter_bp
from case_finder import case_finder_bp
from adversarial_argument_generator import adversary_bp
import subprocess
import os
import sys
import threading
import time

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Register blueprints
app.register_blueprint(summary_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(pdfqa_bp)
app.register_blueprint(drafter_bp)
app.register_blueprint(case_finder_bp)
app.register_blueprint(adversary_bp)

# Global variable to track bot process
bot_process = None
bot_status = {"running": False, "message": "Bot not started"}

# Frontend routes
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

def run_bot():
    global bot_process, bot_status
    try:
        bot_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'telegram_bot.py')
        bot_process = subprocess.Popen(
            [sys.executable, bot_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        bot_status["running"] = True
        bot_status["message"] = "Bot started successfully"
        print("🤖 Telegram bot started successfully")
        stdout, stderr = bot_process.communicate()
        if bot_process.returncode != 0:
            bot_status["running"] = False
            bot_status["message"] = f"Bot stopped with error: {stderr}"
            print(f"❌ Bot error: {stderr}")
        else:
            bot_status["running"] = False
            bot_status["message"] = "Bot stopped normally"
            print("🛑 Bot stopped")
    except Exception as e:
        bot_status["running"] = False
        bot_status["message"] = f"Failed to start bot: {str(e)}"
        print(f"❌ Error starting bot: {e}")

@app.route('/start-telegram-bot')
def start_telegram_bot():
    global bot_process, bot_status
    if bot_process and bot_process.poll() is None:
        return jsonify({
            "status": "already_running",
            "message": "🤖 Telegram Bot is already running!"
        })
    try:
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        time.sleep(2)
        return jsonify({
            "status": "started",
            "message": "🤖 Telegram Bot Started! Check your terminal for logs."
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"❌ Failed to start bot: {str(e)}"
        })

@app.route('/bot-status')
def get_bot_status():
    global bot_process, bot_status
    if bot_process:
        if bot_process.poll() is None:
            bot_status["running"] = True
        else:
            bot_status["running"] = False
    return jsonify(bot_status)

@app.route('/stop-telegram-bot')
def stop_telegram_bot():
    global bot_process, bot_status
    if bot_process and bot_process.poll() is None:
        try:
            bot_process.terminate()
            bot_process.wait(timeout=10)
            bot_status["running"] = False
            bot_status["message"] = "Bot stopped successfully"
            return jsonify({
                "status": "stopped",
                "message": "🛑 Telegram Bot Stopped"
            })
        except subprocess.TimeoutExpired:
            bot_process.kill()
            bot_status["running"] = False
            bot_status["message"] = "Bot force killed"
            return jsonify({
                "status": "killed",
                "message": "🛑 Telegram Bot Force Stopped"
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"❌ Error stopping bot: {str(e)}"
            })
    else:
        return jsonify({
            "status": "not_running",
            "message": "🤖 Bot is not running"
        })

@app.route('/health')
def health():
    return "✅ Server is running", 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='127.0.0.1', port=port, debug=True)

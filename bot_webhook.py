from flask import Blueprint, request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import os
import google.generativeai as genai

# Create Flask blueprint
bot_bp = Blueprint("bot_webhook", __name__)

# Load bot token from environment variable or paste here
BOT_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_BOT_TOKEN_HERE"
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or "https://yourdomain.com/webhook"

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the bot application
application = Application.builder().token(BOT_TOKEN).build()


# -------- Telegram Bot Handlers -------- #
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to LegalHawk Telegram Bot!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")


# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", start))
application.add_handler(CommandHandler("echo", echo))  # optional


# -------- Flask Route for Telegram Webhook -------- #
@bot_bp.route("/webhook", methods=["POST"])
async def webhook():
    if request.method == "POST":
        try:
            update = Update.de_json(request.get_json(force=True), application.bot)
            await application.process_update(update)
        except Exception as e:
            print(f"❌ Error in webhook: {e}")
        return Response("OK", status=200)

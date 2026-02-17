import os
from dotenv import load_dotenv
import fitz
import requests
from bs4 import BeautifulSoup

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# ---------------- ENV ---------------- #

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in .env")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in .env")

# ---------------- LLM ---------------- #

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_retries=3
)

# ---------------- CONSTANTS ---------------- #

FEATURES = [
    "1. PDF Question Answering",
    "2. PDF Summarization",
    "3. Basic Chatbot",
    "4. Case Finder"
]

user_pdf_texts = {}

# ---------------- START ---------------- #

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[f] for f in FEATURES]

    await update.message.reply_text(
        "AI Legal Assistant\n\nChoose feature:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ---------------- MESSAGE ---------------- #

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == FEATURES[0]:
        context.user_data["awaiting_pdf"] = True
        context.user_data["feature"] = "qa"
        await update.message.reply_text("Send PDF for Q&A")
        return

    if text == FEATURES[1]:
        context.user_data["awaiting_pdf"] = True
        context.user_data["feature"] = "summary"
        await update.message.reply_text("Send PDF for Summary")
        return

    if text == FEATURES[2]:
        context.user_data["feature"] = "chat"
        await update.message.reply_text("Chat mode activated")
        return

    if text == FEATURES[3]:
        context.user_data["feature"] = "case"
        await update.message.reply_text("Send case search query")
        return

    # Chat
    if context.user_data.get("feature") == "chat":
        reply = await llm_chat(text)
        await update.message.reply_text(reply)
        return

    # Case Finder
    if context.user_data.get("feature") == "case":
        cases = await search_cases(text)
        await update.message.reply_text("\n\n".join(cases))
        return

    # PDF Features
    if context.user_data.get("pdf_loaded"):
        pdf_text = user_pdf_texts.get(user_id, "")

        if context.user_data["feature"] == "qa":
            ans = await llm_pdf_qa(text, pdf_text)
            await update.message.reply_text(ans)

        if context.user_data["feature"] == "summary":
            summ = await llm_summary(pdf_text)
            await update.message.reply_text(summ)

# ---------------- PDF ---------------- #

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not context.user_data.get("awaiting_pdf"):
        await update.message.reply_text("Select PDF feature first")
        return

    file = await context.bot.get_file(update.message.document.file_id)
    path = f"{user_id}.pdf"
    await file.download_to_drive(path)

    text = extract_pdf_text(path)
    user_pdf_texts[user_id] = text

    context.user_data["pdf_loaded"] = True
    context.user_data["awaiting_pdf"] = False

    await update.message.reply_text("PDF Loaded. Ask question or request summary.")
    os.remove(path)

# ---------------- PDF TEXT ---------------- #

def extract_pdf_text(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# ---------------- LLM FUNCTIONS ---------------- #

async def llm_chat(msg):
    response = llm.invoke([HumanMessage(content=msg)])
    return response.content


async def llm_pdf_qa(question, pdf_text):
    prompt = f"""
    Answer question using PDF content.

    PDF:
    {pdf_text[:20000]}

    Question:
    {question}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


async def llm_summary(pdf_text):
    prompt = f"""
    Summarize this legal document clearly:

    {pdf_text[:20000]}
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# ---------------- CASE SEARCH ---------------- #

async def search_cases(query):
    url = f"https://indiankanoon.org/search/?formInput={query}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    results = soup.select("div.result")[:5]

    cases = []
    for r in results:
        cases.append(r.get_text(strip=True)[:300])

    return cases if cases else ["No cases found"]

# ---------------- MAIN ---------------- #

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.PDF, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("LangChain Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()

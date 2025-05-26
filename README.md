# ⚖️ AI Legal Assistant

A smart, AI-powered web application that simplifies legal information access. Users can upload legal PDFs to get concise summaries, ask questions about document content, and interact with a general-purpose legal chatbot. The tool also offers legal awareness through curated educational video content.

---

## 🚀 Key Features

- 📄 **PDF Summarizer**  
  Upload legal documents and receive clear summaries with key clauses highlighted (e.g., termination, liability, confidentiality).

- ❓ **PDF-Based Q&A**  
  Ask specific questions about an uploaded legal PDF and get direct, AI-generated answers.

- 💬 **General Legal Chatbot**  
  Get simple, understandable answers to basic legal queries through a conversational AI assistant.

- 🎥 **Legal Awareness Blog**  
  Browse educational legal videos to learn about justice, freedom, rights, and real-world cases.

---

## 🧠 Tech Stack

| Technology         | Purpose                                      |
|--------------------|----------------------------------------------|
| **Flask**          | Backend API for all features                 |
| **HTML + Tailwind**| Clean and responsive frontend UI             |
| **Hugging Face API**| AI-powered chatbot and PDF Q&A              |
| **Tesseract OCR**  | Extract text from scanned or image-based PDFs|
| **LangDetect**     | Filter non-English pages from PDFs           |

---

## 🗂️ Project Structure

ai_legal_assistant_project/
├── app.py                  # Main Flask application that registers routes and blueprints
├── chatbot.py              # Handles /chat route for general legal chatbot (Hugging Face)
├── pdf_qa.py               # Handles /pdf-qa route for answering PDF-specific legal questions
├── summary.py              # Handles /summarize route to summarize uploaded PDFs
├── legal_drafter.py        # (Optional) Generates legal documents via Google Gemini API
│
├── .env                    # Environment variables file (API keys, ignored by Git)
├── .gitignore              # Specifies files and folders to exclude from Git tracking
├── requirements.txt        # Lists Python dependencies to install via pip
│
├── templates/              # All frontend HTML pages served by Flask
│   ├── index.html          # Main homepage with feature navigation
│   ├── blog.html           # Blog page with legal education videos
│   ├── pdf-summary.html    # UI for the PDF summarizer feature
│   ├── pdf-qa.html         # UI for asking questions about uploaded PDFs
│   └── legal-chat.html     # Chat interface for general legal chatbot
│
├── static/                 # (Optional) Folder for CSS, JS, images (if needed)
│   └── style.css           # Example: custom styles
│
├── venv/                   # Python virtual environment (ignored from Git)
│
├── pdfs/                   # (Optional) Folder to temporarily store uploaded PDFs
├── vectorstore/            # (Optional) For storing document embeddings if added later

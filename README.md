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

🗂️ Project Structure (GitHub-Friendly Table Version)
File/Folder	Purpose
app.py	Main Flask app that registers routes and blueprints
chatbot.py	Handles /chat route for the general legal chatbot (Hugging Face)
pdf_qa.py	Handles /pdf-qa route for PDF-specific Q&A
summary.py	Handles /summarize route for summarizing legal PDFs
legal_drafter.py	(Optional) Document drafting via Google Gemini (if used)
.env	API keys and environment variables (excluded from Git)
.gitignore	Specifies files/folders to ignore in Git
requirements.txt	Lists Python package dependencies
templates/	HTML pages served by Flask
├── index.html	Homepage with feature overview
├── blog.html	Page displaying educational legal videos
├── pdf-summary.html	UI for the PDF summarizer tool
├── pdf-qa.html	UI for PDF-based question answering
└── legal-chat.html	UI for general chatbot
static/	(Optional) CSS, JS, images
venv/	Python virtual environment (ignored in Git)
pdfs/	(Optional) Temporary PDF uploads
vectorstore/	(Optional) Embedding store if vector DB is added
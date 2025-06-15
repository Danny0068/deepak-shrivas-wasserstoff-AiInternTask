# ChatTheme Analyzer - AI-Powered Document Insight Tool

An AI-driven web application that allows users to upload and analyze **75+ documents** (PDFs, DOCX, Images with OCR, etc.) and interact with them using **LLM-based theme-focused chat**, complete with **paragraph-level citations** and **context-aware summaries**.

---

##  Key Features

-  Upload and manage 75+ documents of various formats
-  Theme-aware Q&A using advanced LLM (LLaMA 3 70B)
-  Paragraph-level citation in responses for traceability
-  Support for sorting, deletion, and live preview of documents
-  OCR support for scanned PDFs and image files
-  Modular architecture with FastAPI + Streamlit + Docker
-  Graph-based visualization of themes (via Streamlit AGraph)
-  Designed with clean architecture, suitable for production

---

## 🛠️ Tech Stack

| Layer | Stack |
|------|-------|
| Frontend | `Streamlit` |
| Backend | `FastAPI`, `Pydantic`, `Celery`, `Redis` |
| LLM | `LLaMA 3 70B` via Hugging Face Transformers |
| Vector DB | `ChromaDB` |
| File Processing | `PyMuPDF`, `python-docx`, `Pillow`, `pytesseract`, `pdf2image` |
| Deployment | `Docker`, local Redis (dev), Render (optional), Hugging Face Spaces |

---

## Folder Structure (Clean Architecture)

chatbot_analyzer/
├── backend/
│   ├── app/
│   │   ├── api/                    # FastAPI routes
│   │   │   ├── document_router.py       # Upload, delete, list documents
│   │   │   └── query_router.py          # Theme-based Q&A and citation API
│   │   ├── services/               # Business logic
│   │   │   ├── extractor.py              # File-type-based text extraction
│   │   │   ├── embedding.py              # ChromaDB vector indexing and querying
│   │   │   ├── citation.py               # Paragraph-level citation extraction
│   │   │   └── file_manager.py           # File save, delete, path handling
│   │   ├── ingestion/              # File preprocessing utilities
│   │   │   ├── ocr_utils.py              # OCR using Tesseract / EasyOCR
│   │   │   ├── pdf_utils.py              # PDF text extraction (PyMuPDF, pdfplumber)
│   │   │   ├── docx_utils.py             # Word document parser (python-docx)
│   │   │   ├── utils.py                  # Common utilities (text cleaner, splitter)
│   │   │   └── manager.py                # Unified file processing manager
│   │   ├── core/                   # App core configs and logger
│   │   │   ├── config.py                # Constants and .env loader
│   │   │   ├── logger.py                # Logging setup
│   │   │   └── celery_worker.py 


---

## 📄 Current Status

| Module                | Status                                                              |
|-----------------------|---------------------------------------------------------------------|
| File Ingestion        | ✅ Functional for PDF, PNG, DOCX (LibreOffice fallback in progress) |
| OCR                   | ✅ Implemented using `pytesseract`                                  |
| LLM Q&A               | ✅ Working with paragraph-level citation                            |
| Theme Summarization   | ✅ Initial version using embedding clustering                       |
| Streamlit Frontend    | ✅ Document viewer, file manager, chat UI                           |
| Deployment            | ⚙️ Dockerization in progress                                        |
| DOCX-to-PDF           | 🔄 Strategy pending (external API or containerized LibreOffice)     |

---

## 🧪 How to Run (Local Dev)

```bash
# Clone the repo
git clone https://github.com/your-username/chat-theme-analyzer.git
cd chat-theme-analyzer

# Create and activate virtualenv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd backend

pip install -r requirements.txt

# Start FastAPI backend
uvicorn main:app --reload

# Open a new terminal and start Streamlit
cd ../frontend
streamlit run app.py

## LLM 
Tech Stack
LLM: LLaMA 3 70B (can be swapped with smaller model if needed)

Powered by Hugging Face Transformers

Citations matched using similarity + regex on paragraph metadata

Pending Clarifications
Currently evaluating the best approach for .docx to .pdf conversion:

Containerized LibreOffice

External APIs (if available)

Final direction depends on technical feasibility + deployment constraints

Author
Deepak Shrivas 

Email: dannyshirvas31@gmail.com

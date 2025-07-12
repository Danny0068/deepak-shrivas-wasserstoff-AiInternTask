import uuid
import logging
from typing import List, Dict
from langchain_docling import DoclingLoader

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M"
)

def parse_pdf(pdf_path: str, document_name: str, user_id: str):
    try:
        loader = DoclingLoader(file_path=[pdf_path], export_type="doc_chunks")
        docs = loader.load()
        parsed_content = []
        for chunk in docs:
            para_data = {
                "paragraph_id": str(uuid.uuid4()),
                "text": chunk.page_content.strip(),
                "page": chunk.metadata.get("page", 0),
                "section": chunk.metadata.get("section"),
                "is_heading": chunk.metadata.get("is_heading", False),
                "document_name": document_name,
                "user_id": user_id,
                # Optionally add char_start/char_end if available in metadata
            }
            if para_data["text"]:
                parsed_content.append(para_data)
        logger.info(f"PDF parsed {len(parsed_content)} paragraphs from {document_name}")
        return parsed_content
    except Exception as e:
        logger.exception(f"[PDF PARSER ERROR] Failed to parse {document_name}: {e}")
        return []
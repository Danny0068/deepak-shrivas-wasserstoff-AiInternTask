import uuid
import logging
from typing import List, Dict
from langchain_docling import DoclingLoader

logger = logging.getLogger(__name__)

def parse_docx(docx_path: str, document_name: str, user_id: str) -> List[Dict]:
    try:
        loader = DoclingLoader(file_path=[docx_path], export_type="doc_chunks")
        docs = loader.load()
        parsed_docx = []

        for chunk in docs:
            para_data = {
                "paragraph_id": str(uuid.uuid4()),
                "text": chunk.page_content.strip(),
                "page": chunk.metadata.get("page", 0),
                "section": chunk.metadata.get("section"),
                "is_heading": chunk.metadata.get("is_heading", False),
                "document_name": document_name,
                "user_id": user_id,
            }
            if para_data["text"]:
                parsed_docx.append(para_data)

        logger.info(f"DOCX parsed {len(parsed_docx)} paragraphs from {document_name}")
        return parsed_docx

    except Exception as e:
        logger.exception(f"[DOCX PARSER ERROR] Failed to parse {document_name}: {e}")
        return []

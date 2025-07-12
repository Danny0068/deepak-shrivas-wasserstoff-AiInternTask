import os
import logging
from typing import List, Dict
from pathlib import Path
from .pdf_parser import parse_pdf
from .docs_parser import parse_docx
from .ocr_parser import parse_ocr_file

logger = logging.getLogger(__name__)

SUPPORTED_FILE_TYPES = {
    ".pdf": "pdf",
    ".docx": "docx",
    ".jpeg": "image",
    ".jpg": "image",
    ".png": "image",
    ".tiff": "image"
}

def process_file(file_path: str, document_name: str, user_id: str) -> List[Dict]:
    """
    Routes the file to the correct parsing utility based on its type.
    Handles normal PDFs, scanned PDFs, DOCX, and image files.
    Returns:
        List[Dict]: Parsed paragraphs with metadata.
    """
    try:
        ext = Path(file_path).suffix.lower()

        if ext not in SUPPORTED_FILE_TYPES:
            logger.error(f"Unsupported file type: {ext} for {document_name}")
            raise ValueError(f"Unsupported file type: {ext}")

        file_type = SUPPORTED_FILE_TYPES[ext]
        logger.info(f"Processing file: {document_name} as type: {file_type}")

        if file_type == "pdf":
            parsed = parse_pdf(file_path, document_name, user_id)

            if parsed and len(parsed) > 0:
                logger.info(f"Successfully parsed normal PDF: {document_name} with {len(parsed)} paragraphs.")
                return parsed
            else:
                logger.warning(f"No text found in PDF, falling back to OCR for: {document_name}")
                parsed_ocr = parse_ocr_file(file_path, document_name, user_id)
                logger.info(f"OCR parsed {len(parsed_ocr)} paragraphs from {document_name}")
                return parsed_ocr

        elif file_type == "docx":
            parsed = parse_docx(file_path, document_name, user_id)
            logger.info(f"Parsed {len(parsed)} paragraphs from DOCX: {document_name}")
            return parsed

        elif file_type == "image":
            parsed = parse_ocr_file(file_path, document_name, user_id)
            logger.info(f"Parsed {len(parsed)} paragraphs from image file: {document_name}")
            return parsed

        else:
            logger.error(f"No parser defined for file type: {file_type}")
            raise ValueError(f"No parser defined for file type: {file_type}")

    except Exception as e:
        logger.exception(f"[MANAGER ERROR] Failed processing {document_name}: {e}")
        return []

import uuid
import logging
from typing import List, Dict
from pathlib import Path
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

def parse_ocr_file(
    file_path: str,
    document_name: str,
    user_id: str,
    lang: str = "eng",
    min_paragraph_length: int = 10
) -> List[Dict]:
    """
    Handles both scanned PDFs and image files for OCR.
    Supports: PDF, JPG, JPEG, PNG, TIFF

    Returns:
        List[Dict]: Paragraph-level OCR output with metadata.
    """
    try:
        ext = Path(file_path).suffix.lower()

        if ext == ".pdf":
            images = convert_from_path(file_path)
        elif ext in [".jpg", ".jpeg", ".png", ".tiff"]:
            images = [Image.open(file_path)]
        else:
            logger.error(f"Unsupported file type for OCR: {ext}")
            raise ValueError(f"Unsupported file type for OCR: {ext}")

        parsed = []

        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang=lang)
            paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) >= min_paragraph_length]

            char_offset = 0
            for p in paragraphs:
                para_data = {
                    "paragraph_id": str(uuid.uuid4()),
                    "text": p,
                    "page": i + 1,
                    "section": None,
                    "is_heading": False,
                    "document_name": document_name,
                    "user_id": user_id,
                    "char_start": char_offset,
                    "char_end": char_offset + len(p)
                }
                char_offset += len(p) + 2
                parsed.append(para_data)

        logger.info(f"OCR extracted {len(parsed)} paragraphs from {document_name}")
        return parsed

    except Exception as e:
        logger.exception(f"[OCR PARSER ERROR] Failed to OCR {document_name}: {e}")
        return []

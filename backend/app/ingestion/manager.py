from pathlib import Path
import shutil
from .convert_to_pdf_utils import convert_docs_to_pdf, convert_image_to_pdf
from .pdf_utils import extract_text_with_citations_from_pdf
from .utils import (
    get_file_hash,
    format_file_size,
    get_file_metadata,
    ensure_dir,
    sanitize_filename,
    is_supported_file
)

STORAGE_DIR = "filestorage"

def process_file(file_path: str, user_id: str) -> dict:
    file_path = Path(file_path)

    if not is_supported_file(str(file_path)):
        raise ValueError(f"Unsupported file type: {file_path.suffix}")

    # Ensure user storage directory exists
    user_storage = Path(STORAGE_DIR) / sanitize_filename(user_id)
    ensure_dir(str(user_storage))

    # Copy original file to user-specific storage if not already there
    file_hash = get_file_hash(str(file_path))
    ext = file_path.suffix.lower()
    sanitized_name = sanitize_filename(file_path.stem)
    stored_file_name = f"{file_hash}_{sanitized_name}{ext}"
    stored_path = user_storage / stored_file_name

    if not stored_path.exists():
        if file_path.resolve() != stored_path.resolve():
            shutil.copy2(str(file_path), str(stored_path))

    # Final PDF path to be reused if already converted
    converted_pdf_path = user_storage / f"{file_hash}_{sanitized_name}.pdf"

    # Convert to PDF if necessary (skip if already converted)
    if converted_pdf_path.exists():
        pdf_path = str(converted_pdf_path)
    else:
        if ext in ['.docx', '.doc']:
            pdf_path = convert_docs_to_pdf(str(stored_path), str(user_storage))
        elif ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.webp']:
            pdf_path = convert_image_to_pdf(str(stored_path), str(converted_pdf_path))
        elif ext == '.pdf':
            pdf_path = str(stored_path)
        else:
            raise RuntimeError("Unsupported file format for conversion.")

    # Extract text with citations
    text_with_citations = extract_text_with_citations_from_pdf(pdf_path)

    print(f"[INFO] Processed file: {stored_path}")
    print(f"[INFO] PDF version stored at: {pdf_path}")

    return {
        "user_id": user_id,
        "file_hash": file_hash,
        "file_path": str(stored_path),
        "metadata": get_file_metadata(pdf_path),
        "text_with_citations": text_with_citations,
        "file_size": format_file_size(pdf_path)
    }

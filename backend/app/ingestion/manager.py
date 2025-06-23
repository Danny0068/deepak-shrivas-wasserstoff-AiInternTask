from pathlib import Path
import shutil
from .convert_to_pdf_utils import convert_image_to_pdf
from .pdf_utils import extract_text_with_citations_from_pdf
from .docs_utils import docs_to_text_with_citaitons
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

    # Process based on file type
    if ext in ['.docx', '.doc']:
        text_with_citations = docs_to_text_with_citaitons(str(stored_path), sanitized_name, user_id)
    else:
        # Convert to PDF if needed
        converted_pdf_path = user_storage / f"{file_hash}_{sanitized_name}.pdf"
        if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.webp']:
            if not converted_pdf_path.exists():
                convert_image_to_pdf(str(stored_path), str(converted_pdf_path))
            pdf_path = str(converted_pdf_path)
        elif ext == '.pdf':
            pdf_path = str(stored_path)
        else:
            raise RuntimeError("Unsupported file format for conversion.")

        # Extract citations from PDF
        text_with_citations = extract_text_with_citations_from_pdf(pdf_path, sanitized_name, user_id)

    return {
        "user_id": user_id,
        "file_hash": file_hash,
        "file_path": str(stored_path),
        "metadata": get_file_metadata(str(stored_path)),
        "text_with_citations": text_with_citations,
        "file_size": format_file_size(str(stored_path))
    }

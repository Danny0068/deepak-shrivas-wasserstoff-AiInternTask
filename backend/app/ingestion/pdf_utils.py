import fitz  # PyMuPDF

def extract_text_with_citations_from_pdf(path: str, document_name: str = "", user_id: str = "") -> list[dict]:
    """
    Extract text from a PDF with page and paragraph numbers, and optionally group lines into logical paragraphs.

    Args:
        path (str): Path to the PDF file.
        document_name (str): Optional document name.
        user_id (str): Optional user ID.

    Returns:
        List[dict]: List of extracted text chunks with citation metadata.
    """
    doc = fitz.open(path)
    results = []
    group_lines_into_paragraphs = True  # Toggle this for finer paragraph merging

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        raw_lines = [line.strip() for line in text.split("\n")]
        
        # Filter empty/noisy lines
        lines = [line for line in raw_lines if line and (len(line) > 3 or any(char.isalnum() for char in line))]

        # Optionally group short lines into logical paragraphs
        if group_lines_into_paragraphs:
            paragraphs = []
            buffer = []
            for line in lines:
                buffer.append(line)
                if len(" ".join(buffer)) > 80:  # You can tune this threshold
                    paragraphs.append(" ".join(buffer))
                    buffer = []
            if buffer:
                paragraphs.append(" ".join(buffer))
        else:
            paragraphs = lines

        for para_num, para_text in enumerate(paragraphs, start=1):
            results.append({
                "user_id": user_id,
                "document_name": document_name,
                "page": page_num,
                "paragraph": para_num,
                "text": para_text
            })

    return results
import fitz  # PyMuPDF

def extract_text_with_citations_from_pdf(path: str, document_name: str, user_id: str) -> list[dict]:
    """
    Extracts paragraph-level text blocks from a PDF with user and document metadata.

    Args:
        path (str): Path to the PDF.
        document_name (str): Logical name of the document (for grouping).
        user_id (str): ID of the user who uploaded the document.

    Returns:
        List[dict]: Each dict contains 'user_id', 'document_name', 'page', 'paragraph', 'text'.
    """
    doc = fitz.open(path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        try:
            # Extract blocks and sort top-down, left-right
            blocks = page.get_text("blocks")
            blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # sort by y, then x

            for para_num, block in enumerate(blocks, start=1):
                text = block[4].strip()
                if text:
                    results.append({
                        "user_id": user_id,
                        "document_name": document_name,
                        "page": page_num,
                        "paragraph": para_num,
                        "text": text
                    })
        except Exception as e:
            results.append({
                "user_id": user_id,
                "document_name": document_name,
                "page": page_num,
                "paragraph": -1,
                "text": f"[ERROR extracting text on page {page_num}: {str(e)}]"
            })

    return results

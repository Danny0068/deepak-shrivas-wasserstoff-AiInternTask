from docx import Document
from typing import List, Dict


def get_avg_font_size(para) -> float:
    """Get average font size across all runs in a paragraph."""
    sizes = [run.font.size.pt for run in para.runs if run.font.size]
    return sum(sizes) / len(sizes) if sizes else 11.0  # Default Word font size


def is_heading(para, prev_font: float, next_font: float) -> bool:
    """Heuristic to determine if a paragraph is likely a heading."""
    text = para.text.strip()
    word_count = len(text.split())
    bold = any(run.bold for run in para.runs)
    font_size = get_avg_font_size(para)

    return (
        bool(text)
        and word_count <= 10
        and font_size > prev_font + 1.0
        and font_size >= next_font
        and bold
    )


def docs_to_text_with_citaitons(docx_path: str, document_name: str, user_id: str) -> List[Dict]:
    """
    Extract structured text with simulated page and paragraph numbers from a DOCX file.

    Args:
        docx_path (str): Path to the .docx file.
        document_name (str): Name of the document (for metadata/citations).
        user_id (str): ID of the user (to track ownership).

    Returns:
        List[Dict]: List of extracted paragraphs with simulated page and paragraph numbers.
    """
    doc = Document(docx_path)
    paragraphs = doc.paragraphs
    results = []

    current_page = 0
    para_number = 1

    for i, para in enumerate(paragraphs):
        text = para.text.strip()
        if not text:
            continue

        prev_font = get_avg_font_size(paragraphs[i - 1]) if i > 0 else get_avg_font_size(para)
        next_font = get_avg_font_size(paragraphs[i + 1]) if i < len(paragraphs) - 1 else get_avg_font_size(para)

        if is_heading(para, prev_font, next_font):
            current_page += 1
            para_number = 1

        results.append({
            "user_id": user_id,
            "document_name": document_name,
            "page": current_page,
            "paragraph": para_number,
            "text": text
        })
        para_number += 1

    return results

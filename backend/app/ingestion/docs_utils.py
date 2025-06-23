from docx import Document
from pathlib import Path

def docs_to_text_with_citaitons(path:str, document_name: str, user_id:str)-> list[dict]:
    """
    Extracts Text From a DOCX file with custom filters,
    heading,
    line breaks,
    line spacing
    """
    doc = Document(path)
    results=[]
    current_page = 1
    para_counter = 0
    blank_count = 0
    for para in doc.paragraphs:
        text = para.text.strip()
        style = para.style.name.lower()
        if not text:
            blank_count +=1 
            continue 
        else:
            blank_count = 0
    
    if 'heading' in style or 'title' in style or text.isupper() or len(text.split()) <= 3  or blank_count > 2:
        current_page += 1
        para_counter = 0

    
    para_counter += 1 
    results.append({
        "user_id": user_id,
        "document_name": document_name,
        "page": current_page,
        "paragraph": para_counter,
        "text": text
    })
    return results
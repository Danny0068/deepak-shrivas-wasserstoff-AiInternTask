import os 
import subprocess
from pathlib import Path
from typing import Optional 
from PIL import Image 
import pytesseract


def convert_image_to_pdf(image_path:str, output_path:str) -> Optional[str]:
    """
    Convert an imgae (scanned document to searchable pdf using pytesseract 
    retunr the path to the generated PDF file or None if conversion fails """

    try:
        image = Image.open(image_path)
        pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')

        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok = True)

        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)
            return output_path
    except Exception as e:
        print(f"[EXCEPTION] Error converting {image_path} to PDF: {e}")
        return None
    return None


        
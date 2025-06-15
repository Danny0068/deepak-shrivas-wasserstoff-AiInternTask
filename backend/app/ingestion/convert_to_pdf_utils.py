import os 
import subprocess
from pathlib import Path
from typing import Optional 
from PIL import Image 
import pytesseract

def convert_docs_to_pdf(docx_path:str, output_dir:str) -> Optional[str]:
    """
    Convert a DOX file to PDF using LiberOffice in headless mode.
    returns the path to the genrated PDF file or None if conversion Fails"""
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        result = subprocess.run(
            ['libreoffice','--headless','--convert-to','pdf', docx_path, '--outdir',str(output_path)],
            stdout = subprocess.PIPE,stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            pdf_name = Path(docx_path).with_suffix(',pdf').name # 
            return str(Path(output_dir)/pdf_name) # return the path to the generated PDF file 
        else:
            print(f"Error converting {docx_path} to PDF: {result.stderr.decode()}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] Error Converting {docx_path} to PDF:{e}")
        return None 

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


        
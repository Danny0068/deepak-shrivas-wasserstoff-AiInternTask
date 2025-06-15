import hashlib
import os 
from pathlib import Path
from datetime import datetime

# hash fuction to get the MD5 hash of a file 
def get_file_hash(file_path: str) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Function to format file size in a human-readable format
def format_file_size(file_path: str) -> str:
    size_bytes = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
# Function to get metadata of a file
def get_file_metadata(file_path: str) -> dict:
    path = Path(file_path)
    return {
        "name": path.name,
        "extension": path.suffix.lower(),
        "size": format_file_size(file_path),
        "created": datetime.fromtimestamp(path.stat().st_ctime).isoformat()
    }
# Function to ensure a directory exists
def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)
# Function to sanitize filenames
def sanitize_filename(name: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)
# Function to check if a file is supported for processing
def is_supported_file(file_path: str) -> bool:
    supported = ['.pdf', '.docx', '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif', '.webp']
    return Path(file_path).suffix.lower() in supported

from werkzeug.utils import secure_filename
from pathlib import Path

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

def allowed_filename(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, user_folder: Path) -> Path:
    filename = secure_filename(file.filename)
    save_path = user_folder / filename
    file.save(save_path)
    return save_path

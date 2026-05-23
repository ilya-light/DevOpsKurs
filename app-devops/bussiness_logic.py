import glob
from pathlib import Path


ALLOWED_EXTENSIONS = {"py", "txt", "docx", "doc", "pdf", "png", "jpg", "jpeg", "gif"}


def check_password(user, password):
    return user == "admin" and password == "password"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_folder(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def get_files_in_folder(folder):
    return sorted(
        Path(filename).name
        for filename in glob.glob(f"{folder}/*")
        if Path(filename).is_file()
    )

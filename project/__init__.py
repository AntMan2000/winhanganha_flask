import os
from pathlib import Path
from flask import Flask, session, g
from flask_bootstrap import Bootstrap5
from flask_mysqldb import MySQL



BASE_DIR = Path(__file__).resolve().parent.parent


def load_env_to_dict(env_path):
    env_values = {}

    if not env_path.exists():
        return env_values

    with env_path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value.startswith(("'", '"'))
            ):
                value = value[1:-1]

            env_values[key] = value

    return env_values


env = load_env_to_dict(BASE_DIR / ".env")

upload_folder = BASE_DIR / "project" / "static" / "uploads"
os.makedirs(upload_folder, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "txt", "pdf", "png", "jpg", "jpeg", "gif",
    "doc", "docx", "xls", "xlsx", "ppt", "pptx",
    "csv", "zip", "rar", "7z", "tar", "gz",
    "mp3", "mp4", "avi", "mkv"
}

ALLOWED_IMG_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif"
}

def file_type(path):
    if not path:
        return "none"

    ext = os.path.splitext(path)[1].lower().replace(".", "")

    image_types = {"png", "jpg", "jpeg", "gif", "webp"}
    pdf_types = {"pdf"}
    video_types = {"mp4", "webm", "ogg", "avi", "mkv"}
    audio_types = {"mp3", "wav", "ogg", "m4a"}
    document_types = {"doc", "docx", "txt", "rtf"}
    spreadsheet_types = {"xls", "xlsx", "csv"}
    presentation_types = {"ppt", "pptx"}
    archive_types = {"zip", "rar", "7z", "tar", "gz"}

    if ext in image_types:
        return "image"
    if ext in pdf_types:
        return "pdf"
    if ext in video_types:
        return "video"
    if ext in audio_types:
        return "audio"
    if ext in document_types:
        return "document"
    if ext in spreadsheet_types:
        return "spreadsheet"
    if ext in presentation_types:
        return "presentation"
    if ext in archive_types:
        return "archive"

    return "file"

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = upload_folder
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["ALLOWED_IMG_EXTENSIONS"] = ALLOWED_IMG_EXTENSIONS

###############################################################################################################
###############################################################################################################
## update parameters to suit environment
app.config["SECRET_KEY"] = "SuperSecretKeyForSessionManagement13579"
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_PORT"] = 3307
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "winhanganha_archive"

app.config["FLASK_RUN_HOST"] = "127.0.0.1"
app.config["FLASK_RUN_PORT"] = 1337
## must be false on submission
app.config["FLASK_DEBUG"] = False 

## end of parameter updates
###############################################################################################################
###############################################################################################################


app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_CHARSET"] = "utf8mb4"

mysql = MySQL(app)
bootstrap = Bootstrap5(app)

from project import models
from project import views

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.current_user = None
    else:
        g.current_user = models.load_user(user_id)


@app.context_processor
def inject_current_user():
    from project.models import current_user
    return dict(current_user=current_user)


with app.app_context():
    models.Role.insert_roles()


@app.context_processor
def inject_permissions():
    from project.models import Permission
    return dict(Permission=Permission)


app.jinja_env.globals.update(file_type=file_type)
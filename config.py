import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

os.makedirs(os.path.join(BASE_DIR, "instance"), exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "peixotinhos-dev-key-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "peixotinhos.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

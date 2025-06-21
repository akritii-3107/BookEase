# config_template.py
import os
basedir = os.path.abspath(os.path.dirname(__file__))

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "your_admin_password")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")

theater_upload = os.path.join(basedir, "../uploads/theater_imgs")
show_upload = os.path.join(basedir, "../uploads/show_imgs")

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../database")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "ticket-booking_database.sqlite3")
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key-placeholder")
    SECURITY_PASSWORD_HASH = "bcrypt"
    THEATER_UPLOAD_FOLDER = theater_upload
    SHOW_UPLOAD_FOLDER = show_upload
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'Asia/Kolkata'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "")
    CELERY_INCLUDE = ['app']
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 120

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # safe: loads .env in deployment only if present


class Config:
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", "15")))
    REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRES_DAYS", "7")))

    # Rate limiting
    RATELIMIT_HEADERS_ENABLED = True
    RATE_LIMIT_AUTH = os.getenv("RATE_LIMIT_AUTH", "5 per minute")

    # Security hardening
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # requires HTTPS in production
    PREFERRED_URL_SCHEME = "https"

    # Application
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


def get_config(env: str = None):
    env = env or os.getenv("FLASK_ENV", "production")
    if env == "development":
        return DevelopmentConfig
    return ProductionConfig

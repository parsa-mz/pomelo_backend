import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DB_URL: str = os.getenv("DB_URL")

    APP_VERSION: str = "1.1.0"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_DAYS: int = 14
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class DevSettings(Settings):
    ENV: str = "dev"


class ProdSettings(Settings):
    ENV: str = "prod"
    DEBUG: bool = False

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    WORKERS: int = 4

    SENTRY_DSN: str = os.getenv("SENTRY_DSN")


def get_settings():
    env = os.getenv("ENV", "dev")
    config_type = {
        "dev": DevSettings(),
        "prod": ProdSettings(),
    }
    return config_type[env]


settings: Settings = get_settings()

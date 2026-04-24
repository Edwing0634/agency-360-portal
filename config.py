"""Application configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-in-production")
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "agency360_db")
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_DRIVER: str = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    COMPANY_DOMAIN: str = os.getenv("COMPANY_DOMAIN", "agency360.com")
    APP_TITLE: str = os.getenv("APP_TITLE", "360 Agency Portal")
    WINDOW_WIDTH: int = int(os.getenv("WINDOW_WIDTH", "1280"))
    WINDOW_HEIGHT: int = int(os.getenv("WINDOW_HEIGHT", "800"))
    DEBUG: bool = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    @property
    def connection_string(self) -> str:
        if self.DB_USER:
            return (
                f"DRIVER={{{self.DB_DRIVER}}};"
                f"SERVER={self.DB_SERVER};"
                f"DATABASE={self.DB_NAME};"
                f"UID={self.DB_USER};"
                f"PWD={self.DB_PASSWORD};"
            )
        return (
            f"DRIVER={{{self.DB_DRIVER}}};"
            f"SERVER={self.DB_SERVER};"
            f"DATABASE={self.DB_NAME};"
            "Trusted_Connection=yes;"
        )


config = Config()

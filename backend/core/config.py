import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(env_path)


class Settings:
    def __init__(self):
        self.PROJECT_NAME = "FinSight"
        self.PROJECT_VERSION = "1.0.0"

        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")

        self.DATABASE_URL = (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
        )


settings = Settings()

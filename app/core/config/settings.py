import os
from dotenv import load_dotenv

load_dotenv('dev.env')


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    DEBUG: bool = os.getenv("DEBUG")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL")

    POSTGRES_NAME = os.getenv("POSTGRES_NAME")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_HOST = os.getenv("DATABASE_HOST")

    #DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{POSTGRES_DB}"
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_NAME}:{DATABASE_PORT}/{POSTGRES_DB}"

import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Project directories
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
LOG_DIR = "logs"


# Database configuration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
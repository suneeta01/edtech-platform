from dotenv import load_dotenv
import os

load_dotenv()   # 🔥 THIS LINE IS MISSING

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret")

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")
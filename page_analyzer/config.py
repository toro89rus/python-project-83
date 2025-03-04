import os

from dotenv import load_dotenv

URL_MAX_LEN = 255

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

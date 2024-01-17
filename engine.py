from sqlalchemy import create_engine
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@127.0.0.1:5432/{os.getenv('POSTGRES_DB')}"
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

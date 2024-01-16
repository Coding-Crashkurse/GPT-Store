from fastapi import FastAPI, Path

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class YouTubeVideo(Base):
    __tablename__ = "youtube_videos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    timestamp = Column(DateTime)


class UdemyCourse(Base):
    __tablename__ = "udemy_courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    promocode = Column(String)


Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/promotions")
async def read_promotions():
    return {"message": "Promotions data"}


@app.get("/youtube/{language}")
async def read_youtube(
    language: str = Path(
        ..., title="The language of the content", enum=["all", "english", "german"]
    )
):
    return {"message": f"Youtube content in {language} language"}

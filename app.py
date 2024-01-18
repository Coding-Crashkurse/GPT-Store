from fastapi import FastAPI, Path, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from models import (
    Base,
    YouTubeVideo,
    UdemyCourse,
)


CONNECTION_STRING = "postgresql+psycopg2://myuser:mypw@postgres:5432/mydb"

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint, um YouTube-Videos basierend auf der Sprache abzurufen
@app.get("/youtube/{language}")
async def read_youtube(
    language: str = Path(
        ..., title="The language of the content", enum=["all", "english", "german"]
    ),
    db: Session = Depends(get_db),
):
    if language == "all":
        videos = db.query(YouTubeVideo).all()
    else:
        videos = db.query(YouTubeVideo).filter(YouTubeVideo.language == language).all()

    if not videos:
        raise HTTPException(status_code=404, detail="Videos not found")

    return {
        "videos": [
            dict(
                title=video.title,
                description=video.description,
                language=video.language,
            )
            for video in videos
        ]
    }


@app.get("/promotions")
async def read_promotions():
    session = Session()
    try:
        promotions = session.query(UdemyCourse).all()
        return promotions
    except Exception as e:
        return {"error": str(e)}
    finally:
        session.close()



from fastapi import FastAPI, Path, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from models import (
    Base,
    YouTubeVideo,
    UdemyCourse,
)  # Stellen Sie sicher, dass diese Modelle definiert sind

from dotenv import load_dotenv

load_dotenv()

# Datenbank-URL aus den Umgebungsvariablen laden
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"

# SQLAlchemy Engine und Sessionmaker erstellen
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Erstellen der Datenbanktabellen
Base.metadata.create_all(bind=engine)

# FastAPI App-Instanz
app = FastAPI()


# Dependency, um eine Datenbanksession zu bekommen
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
                timestamp=video.timestamp,
                language=video.language,
            )
            for video in videos
        ]
    }


# Einfacher Endpoint, um Promotions-Daten abzurufen
@app.get("/promotions")
async def read_promotions():
    return {"message": "Promotions data"}


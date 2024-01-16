from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from app import YouTubeVideo, UdemyCourse
import os
from dotenv import load_dotenv

load_dotenv()  # Lädt die Umgebungsvariablen aus der .env-Datei

DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost/{os.getenv('POSTGRES_DB')}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def create_fake_data(session, num_entries=10):
    fake = Faker()

    for _ in range(num_entries):
        # Erstellen von Fake-Daten für YouTubeVideo
        youtube_video = YouTubeVideo(
            title=fake.sentence(), description=fake.text(), timestamp=fake.date_time()
        )
        session.add(youtube_video)

        # Erstellen von Fake-Daten für UdemyCourse
        udemy_course = UdemyCourse(
            title=fake.sentence(), promocode=fake.lexify(text="??????")
        )
        session.add(udemy_course)

    session.commit()


if __name__ == "__main__":
    session = Session()
    create_fake_data(session, num_entries=50)  # Erstellt 50 Einträge für jede Tabelle

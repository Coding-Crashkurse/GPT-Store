import scrapetube
from sqlalchemy.orm import sessionmaker

from engine import engine
from models import UdemyCourse, YouTubeVideo

Session = sessionmaker(bind=engine)


def clear_tables():
    session = Session()
    try:
        session.query(YouTubeVideo).delete()
        session.query(UdemyCourse).delete()
        session.commit()
    except Exception as e:
        print(f"Error clearing tables: {e}")
        session.rollback()
    finally:
        session.close()


def add_udemy_courses():
    session = Session()
    try:
        courses = [
            {
                "title": "LangChain on Azure - Building Scalable LLM Applications",
                "promocode": None,
            },
            {
                "title": "LangChain in Action: Develop LLM-Powered Applications",
                "promocode": None,
            },
            {
                "title": "FastAPI für Anfänger - Baue einen Twitter Clone mit FastAPI",
                "promocode": None,
            },
            {"title": "Data Wrangling mit dem Tidyverse", "promocode": None},
        ]

        for course in courses:
            new_course = UdemyCourse(
                title=course["title"], promocode=course["promocode"]
            )
            session.add(new_course)

        session.commit()
    except Exception as e:
        print(f"An error occurred while adding Udemy courses: {e}")
        session.rollback()
    finally:
        session.close()


def store_channel_videos(channel_url, language):
    session = Session()
    try:
        channel_id = channel_url.split("/")[-1]
        videos = scrapetube.get_channel(channel_id)

        for video in videos:
            title = (
                video.get("title", {}).get("runs", [{}])[0].get("text", "Kein Titel")
            )
            description = (
                video.get("descriptionSnippet", {})
                .get("runs", [{}])[0]
                .get("text", "Keine Beschreibung")
            )
            print(f"Title {title} wird {language} verarbeitet")

            new_video = YouTubeVideo(
                title=title,
                description=description,
                language=language,
            )
            session.add(new_video)
            session.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()


clear_tables()
add_udemy_courses()

deutscher_channel_url = "https://www.youtube.com/channel/UCikLKUS0DZWMkukbkYDG49Q"
englischer_channel_url = "https://www.youtube.com/channel/UCuGxbFmuThl3vWO-tozt43A"

store_channel_videos(deutscher_channel_url, "german")
store_channel_videos(englischer_channel_url, "english")

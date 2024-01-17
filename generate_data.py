from pytube import Channel
from sqlalchemy.orm import sessionmaker
from models import YouTubeVideo
from engine import engine
import scrapetube

Session = sessionmaker(bind=engine)


def store_channel_videos(channel_url, language):
    session = Session()
    try:
        # Extrahieren der Channel-ID aus der URL
        channel_id = channel_url.split("/")[-1]

        # Verwenden von scrapetube, um Videos abzurufen
        videos = scrapetube.get_channel(channel_id)
        print("LENGTH VIDEOS: ", len(list(videos)))

        for video in videos:
            # Standardwerte verwenden, falls bestimmte Schlüssel fehlen
            title = (
                video.get("title", {}).get("runs", [{}])[0].get("text", "Kein Titel")
            )
            description = (
                video.get("descriptionSnippet", {})
                .get("runs", [{}])[0]
                .get("text", "Keine Beschreibung")
            )

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


deutscher_channel_url = "https://www.youtube.com/channel/UCikLKUS0DZWMkukbkYDG49Q"
englischer_channel_url = "https://www.youtube.com/channel/UCuGxbFmuThl3vWO-tozt43A"

store_channel_videos(deutscher_channel_url, "German")
store_channel_videos(englischer_channel_url, "English")

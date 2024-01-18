from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class YouTubeVideo(Base):
    __tablename__ = "youtube"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    language = Column(String)


class UdemyCourse(Base):
    __tablename__ = "udemy"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    promocode = Column(String)

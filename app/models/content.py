from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movie_table'
    id = Column(Integer, primary_key=True, index=True)
    trailer_url = Column(String, unique=True)
    main_content_url = Column(String, unique=True)
    is_ready = Column(Boolean, default=False)


class Series(Base):
    __tablename__ = 'series_table'
    id = Column(Integer, primary_key=True, index=True)
    trailer_url = Column(String, unique=True)
    series_summary_url = Column(String, unique=True)
    is_ready = Column(Boolean, default=False)


class Episode(Base):
    __tablename__ = 'episode_table'
    id = Column(Integer, primary_key=True, index=True)
    episode_content_url = Column(String, unique=True)

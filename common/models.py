# SQLAlchemy models for Catalog Service
# services/catalog-service/models.py
import datetime
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class RoleEnum(enum.Enum):
    admin = "admin"
    client = "client"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.client)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    duration_min = Column(Integer)
    image_url = Column(String)
    category = Column(String, index=True)

    favorites = relationship("UserFavorite", back_populates="movie")
    watched = relationship("UserWatched", back_populates="movie")


class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    num_seasons = Column(Integer)
    num_episodes = Column(Integer)
    duration_ep_min = Column(Integer)
    image_url = Column(String)
    category = Column(String, index=True)

    favorites = relationship("UserFavorite", back_populates="series")
    watched = relationship("UserWatched", back_populates="series")


class UserFavorite(Base):
    __tablename__ = "user_favorites"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True, nullable=True)
    series_id = Column(Integer, ForeignKey("series.id"), primary_key=True, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime)

    movie = relationship("Movie", back_populates="favorites")
    series = relationship("Series", back_populates="favorites")


class UserWatched(Base):
    __tablename__ = "user_watched"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True, nullable=True)
    series_id = Column(Integer, ForeignKey("series.id"), primary_key=True, nullable=True)
    watched_at = Column(DateTime, default=datetime.datetime)
    watch_duration_min = Column(Integer)

    movie = relationship("Movie", back_populates="watched")
    series = relationship("Series", back_populates="watched")

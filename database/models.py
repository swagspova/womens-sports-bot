from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
)

from database.db import Base


# =========================================================
# GAME MODEL
# =========================================================

class Game(Base):

    __tablename__ = "games"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    espn_game_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    sport = Column(
        String,
        nullable=False
    )

    league = Column(
        String,
        nullable=False
    )

    game_date = Column(
        DateTime,
        nullable=True
    )

    away_team = Column(
        String,
        nullable=False
    )

    home_team = Column(
        String,
        nullable=False
    )

    away_score = Column(
        Integer,
        nullable=True
    )

    home_score = Column(
        Integer,
        nullable=True
    )

    status = Column(
        String,
        nullable=False
    )

    posted = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# =========================================================
# TWEET MODEL
# =========================================================

class Tweet(Base):

    __tablename__ = "tweets"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    game_id = Column(
        String,
        nullable=False,
        index=True
    )

    tweet_id = Column(
        String,
        nullable=True,
        unique=True
    )

    tweet_type = Column(
        String,
        nullable=False
    )

    tweet_text = Column(
        Text,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    posted_at = Column(
        DateTime,
        nullable=True
    )


# =========================================================
# BOT LOG MODEL
# =========================================================

class BotLog(Base):

    __tablename__ = "bot_logs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    level = Column(
        String,
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
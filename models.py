from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)

from database import Base


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
        nullable=False
    )

    sport = Column(
        String,
        nullable=False
    )

    league = Column(
        String,
        nullable=False
    )

    home_team = Column(
        String,
        nullable=False
    )

    away_team = Column(
        String,
        nullable=False
    )

    home_score = Column(
        Integer,
        nullable=True
    )

    away_score = Column(
        Integer,
        nullable=True
    )

    status = Column(
        String,
        nullable=False
    )

    game_date = Column(
        DateTime,
        nullable=True
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
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
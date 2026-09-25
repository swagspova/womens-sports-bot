from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


def utc_now():
    """Return current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


# ============================================================
# GAME MODEL
# ============================================================

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)

    # ESPN information
    espn_game_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    sport = Column(
        String,
        nullable=False,
        default="basketball",
    )

    league = Column(
        String,
        nullable=False,
        default="wnba",
    )

    # Game information
    game_date = Column(
        DateTime,
        nullable=True,
    )

    away_team = Column(
        String,
        nullable=False,
    )

    home_team = Column(
        String,
        nullable=False,
    )

    away_score = Column(
        Integer,
        default=0,
    )

    home_score = Column(
        Integer,
        default=0,
    )

    status = Column(
        String,
        nullable=True,
    )

    # Publishing state
    posted = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    # ========================================================
    # TOP PLAYER #1
    # ========================================================

    top_player_1_name = Column(
        String,
        nullable=True,
    )

    top_player_1_points = Column(
        Integer,
        nullable=True,
    )

    top_player_1_assists = Column(
        Integer,
        nullable=True,
    )

    top_player_1_rebounds = Column(
        Integer,
        nullable=True,
    )

    # ========================================================
    # TOP PLAYER #2
    # ========================================================

    top_player_2_name = Column(
        String,
        nullable=True,
    )

    top_player_2_points = Column(
        Integer,
        nullable=True,
    )

    top_player_2_assists = Column(
        Integer,
        nullable=True,
    )

    top_player_2_rebounds = Column(
        Integer,
        nullable=True,
    )

    # ========================================================
    # TIMESTAMPS
    # ========================================================

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )


# ============================================================
# TWEET MODEL
# ============================================================

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    game_id = Column(
        Integer,
        nullable=False,
        index=True,
    )

    tweet_id = Column(
        String,
        unique=True,
        nullable=True,
    )

    tweet_type = Column(
        String,
        nullable=False,
        default="final_score",
    )

    tweet_text = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="posted",
    )

    created_at = Column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    posted_at = Column(
        DateTime,
        nullable=True,
    )
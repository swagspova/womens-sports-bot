from sqlalchemy import Column, Integer, String, DateTime

from database.db import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    espn_game_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    game_date = Column(
        DateTime,
        nullable=False
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

    def __repr__(self):
        return (
            f"<Game("
            f"{self.away_team} "
            f"{self.away_score} - "
            f"{self.home_score} "
            f"{self.home_team}"
            f")>"
        )
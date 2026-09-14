from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///womens-sports.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


def init_db():
    """
    Initialize database tables.
    """

    from models import Game, BotLog

    Base.metadata.create_all(bind=engine)

    print("Database initialized")


def get_session():
    """
    Return a new database session.
    """

    return SessionLocal()


def close_session(session):
    """
    Safely close a database session.
    """

    session.close()


def game_exists(session, espn_game_id):
    """
    Check whether a game already exists.
    """

    from models import Game

    game = (
        session.query(Game)
        .filter(Game.espn_game_id == espn_game_id)
        .first()
    )

    return game is not None


def get_game(session, espn_game_id):
    """
    Retrieve a game using ESPN game ID.
    """

    from models import Game

    return (
        session.query(Game)
        .filter(Game.espn_game_id == espn_game_id)
        .first()
    )


def save_game(session, game_data):
    """
    Save a game to the database.

    If the game already exists, return the existing record.
    """

    from models import Game

    existing_game = get_game(
        session,
        game_data["espn_game_id"]
    )

    if existing_game:
        return existing_game

    game = Game(
        espn_game_id=game_data["espn_game_id"],
        sport=game_data["sport"],
        league=game_data["league"],
        home_team=game_data["home_team"],
        away_team=game_data["away_team"],
        home_score=game_data.get("home_score"),
        away_score=game_data.get("away_score"),
        status=game_data["status"],
        game_date=game_data.get("game_date"),
        posted=game_data.get("posted", False)
    )

    session.add(game)
    session.commit()
    session.refresh(game)

    return game


def get_unposted_games(session):
    """
    Return games that have not yet been posted.
    """

    from models import Game

    return (
        session.query(Game)
        .filter(Game.posted == False)
        .all()
    )


def mark_game_posted(session, espn_game_id):
    """
    Mark a game as successfully posted.
    """

    game = get_game(
        session,
        espn_game_id
    )

    if game is None:
        return False

    game.posted = True

    session.commit()

    return True
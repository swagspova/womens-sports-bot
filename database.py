from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import declarative_base, sessionmaker


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE_URL = "sqlite:///womens_sports.db"


engine = create_engine(
    DATABASE_URL,
    echo=False
)


SessionLocal = sessionmaker(
    bind=engine
)


Base = declarative_base()


# ==========================================================
# GAME MODEL
# ==========================================================

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

    date = Column(
        DateTime,
        nullable=True
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

    # 0 = not posted
    # 1 = posted

    posted = Column(
        Integer,
        default=0,
        nullable=False
    )


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def init_db():

    Base.metadata.create_all(engine)

    print("Database initialized")


# ==========================================================
# GET SESSION
# ==========================================================

def get_session():

    return SessionLocal()


# ==========================================================
# SAVE GAME
# ==========================================================

def save_game(session, game_data):
    """
    Save a game to the database.

    If the ESPN Game ID already exists, update the
    existing game instead of creating a duplicate.

    The function accepts the normalized game dictionary
    produced by the WNBA/ESPN parser.
    """

    # ------------------------------------------------------
    # Required field
    # ------------------------------------------------------

    espn_game_id = str(
        game_data["espn_game_id"]
    )


    # ------------------------------------------------------
    # Optional fields
    #
    # These defaults make the database layer compatible
    # with the existing Day 2 test data.
    # ------------------------------------------------------

    sport = game_data.get(
        "sport",
        "wnba"
    )

    league = game_data.get(
        "league",
        "WNBA"
    )

    date = game_data.get(
        "date"
    )

    home_team = game_data.get(
        "home_team",
        ""
    )

    away_team = game_data.get(
        "away_team",
        ""
    )

    home_score = game_data.get(
        "home_score"
    )

    away_score = game_data.get(
        "away_score"
    )

    status = game_data.get(
        "status",
        "unknown"
    )


    # ------------------------------------------------------
    # Check whether game already exists
    # ------------------------------------------------------

    existing_game = (
        session.query(Game)
        .filter(
            Game.espn_game_id == espn_game_id
        )
        .first()
    )


    # ======================================================
    # UPDATE EXISTING GAME
    # ======================================================

    if existing_game:

        existing_game.sport = sport

        existing_game.league = league

        existing_game.date = date

        existing_game.home_team = home_team

        existing_game.away_team = away_team

        existing_game.home_score = home_score

        existing_game.away_score = away_score

        existing_game.status = status

        # Do NOT reset posted.
        #
        # If this game was already tweeted,
        # updating the game must not make it
        # eligible for another tweet.

        session.commit()

        return existing_game


    # ======================================================
    # INSERT NEW GAME
    # ======================================================

    new_game = Game(

        espn_game_id=espn_game_id,

        sport=sport,

        league=league,

        date=date,

        home_team=home_team,

        away_team=away_team,

        home_score=home_score,

        away_score=away_score,

        status=status,

        posted=0,
    )


    session.add(new_game)

    session.commit()

    session.refresh(new_game)

    return new_game

    # ------------------------------------------------------
    # Get ESPN Game ID
    # ------------------------------------------------------

    espn_game_id = str(
        game_data["espn_game_id"]
    )


    # ------------------------------------------------------
    # Look for existing game
    # ------------------------------------------------------

    existing_game = (
        session.query(Game)
        .filter(
            Game.espn_game_id == espn_game_id
        )
        .first()
    )


    # ======================================================
    # UPDATE EXISTING GAME
    # ======================================================

    if existing_game:

        existing_game.sport = (
            game_data["sport"]
        )

        existing_game.league = (
            game_data["league"]
        )

        existing_game.date = (
            game_data["date"]
        )

        existing_game.home_team = (
            game_data["home_team"]
        )

        existing_game.away_team = (
            game_data["away_team"]
        )

        existing_game.home_score = (
            game_data["home_score"]
        )

        existing_game.away_score = (
            game_data["away_score"]
        )

        existing_game.status = (
            game_data["status"]
        )

        # IMPORTANT:
        # Do not change existing_game.posted.
        #
        # If the game has already been tweeted,
        # updating the ESPN score must not make it
        # eligible for another tweet.

        session.commit()

        return existing_game


    # ======================================================
    # INSERT NEW GAME
    # ======================================================

    new_game = Game(

        espn_game_id=espn_game_id,

        sport=game_data["sport"],

        league=game_data["league"],

        date=game_data["date"],

        home_team=game_data["home_team"],

        away_team=game_data["away_team"],

        home_score=game_data["home_score"],

        away_score=game_data["away_score"],

        status=game_data["status"],

        posted=0,
    )


    session.add(new_game)

    session.commit()

    session.refresh(new_game)

    return new_game


# ==========================================================
# GAME EXISTS
# ==========================================================

def game_exists(session, espn_game_id):
    """
    Check whether a game exists.

    Parameters
    ----------
    session:
        SQLAlchemy database session.

    espn_game_id:
        ESPN Game ID.

    Returns
    -------
    bool
        True if game exists.
        False otherwise.
    """

    game = (
        session.query(Game)
        .filter(
            Game.espn_game_id
            == str(espn_game_id)
        )
        .first()
    )

    return game is not None


# ==========================================================
# GET GAME
# ==========================================================

def get_game(session, espn_game_id):
    """
    Get one game using its ESPN Game ID.
    """

    return (
        session.query(Game)
        .filter(
            Game.espn_game_id
            == str(espn_game_id)
        )
        .first()
    )


# ==========================================================
# GET GAME BY ESPN ID
# ==========================================================

def get_game_by_espn_id(session, espn_game_id):
    """
    Alias for get_game().
    """

    return get_game(
        session,
        espn_game_id
    )


# ==========================================================
# GET UNPOSTED GAMES
# ==========================================================

def get_unposted_games(session):
    """
    Return all games that have not yet been posted.

    posted = 0 means not posted.
    posted = 1 means already posted.
    """

    return (
        session.query(Game)
        .filter(
            Game.posted == 0
        )
        .order_by(Game.date)
        .all()
    )


# ==========================================================
# MARK GAME AS POSTED
# ==========================================================

def mark_game_posted(session, espn_game_id):
    """
    Mark a game as posted.
    """

    game = get_game(
        session,
        espn_game_id
    )


    if game is None:

        return False


    game.posted = 1

    session.commit()

    return True


# ==========================================================
# GET ALL GAMES
# ==========================================================

def get_all_games(session):
    """
    Return all games in the database.
    """

    return (
        session.query(Game)
        .order_by(Game.date)
        .all()
    )


# ==========================================================
# COUNT GAMES
# ==========================================================

def count_games(session):
    """
    Return the total number of games.
    """

    return session.query(Game).count()


# ==========================================================
# DELETE GAME
# ==========================================================

def delete_game(session, espn_game_id):
    """
    Delete one game using ESPN Game ID.
    """

    game = get_game(
        session,
        espn_game_id
    )


    if game is None:

        return False


    session.delete(game)

    session.commit()

    return True


# ==========================================================
# DELETE ALL GAMES
# ==========================================================

def delete_all_games(session):
    """
    Delete all games.
    """

    session.query(Game).delete()

    session.commit()


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("WOMEN'S SPORTS BOT DATABASE")
    print("=" * 60)

    init_db()

    print()
    print("Database ready.")
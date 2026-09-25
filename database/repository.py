from datetime import datetime, timezone

from sqlalchemy.orm import Session

from database.models import Game, Tweet


# ============================================================
# TIME
# ============================================================

def utc_now():
    """Return current UTC time as a timezone-aware datetime."""
    return datetime.now(timezone.utc)


# ============================================================
# GAME FUNCTIONS
# ============================================================

def game_exists(db: Session, espn_game_id: str) -> bool:
    """Check whether a game already exists."""

    return (
        db.query(Game)
        .filter(Game.espn_game_id == espn_game_id)
        .first()
        is not None
    )


def save_game(db: Session, game_data: dict) -> Game:
    """
    Save a new game or update an existing game.

    Expected game_data:

    {
        "espn_game_id": "...",
        "sport": "basketball",
        "league": "wnba",
        "game_date": ...,
        "away_team": "...",
        "home_team": "...",
        "away_score": 90,
        "home_score": 85,
        "status": "STATUS_FINAL"
    }
    """

    existing_game = (
        db.query(Game)
        .filter(
            Game.espn_game_id == game_data["espn_game_id"]
        )
        .first()
    )

    # --------------------------------------------------------
    # UPDATE EXISTING GAME
    # --------------------------------------------------------

    if existing_game:

        existing_game.sport = game_data.get(
            "sport",
            existing_game.sport,
        )

        existing_game.league = game_data.get(
            "league",
            existing_game.league,
        )

        existing_game.game_date = game_data.get(
            "game_date",
            existing_game.game_date,
        )

        existing_game.away_team = game_data.get(
            "away_team",
            existing_game.away_team,
        )

        existing_game.home_team = game_data.get(
            "home_team",
            existing_game.home_team,
        )

        existing_game.away_score = game_data.get(
            "away_score",
            existing_game.away_score,
        )

        existing_game.home_score = game_data.get(
            "home_score",
            existing_game.home_score,
        )

        existing_game.status = game_data.get(
            "status",
            existing_game.status,
        )

        existing_game.updated_at = utc_now()

        db.commit()
        db.refresh(existing_game)

        return existing_game

    # --------------------------------------------------------
    # CREATE NEW GAME
    # --------------------------------------------------------

    new_game = Game(
        espn_game_id=game_data["espn_game_id"],
        sport=game_data.get(
            "sport",
            "basketball",
        ),
        league=game_data.get(
            "league",
            "wnba",
        ),
        game_date=game_data.get(
            "game_date"
        ),
        away_team=game_data.get(
            "away_team"
        ),
        home_team=game_data.get(
            "home_team"
        ),
        away_score=game_data.get(
            "away_score",
            0,
        ),
        home_score=game_data.get(
            "home_score",
            0,
        ),
        status=game_data.get(
            "status"
        ),
        posted=False,
        created_at=utc_now(),
        updated_at=utc_now(),
    )

    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game


def get_game(
    db: Session,
    espn_game_id: str,
):
    """Get a game using ESPN's game ID."""

    return (
        db.query(Game)
        .filter(
            Game.espn_game_id == espn_game_id
        )
        .first()
    )


def get_game_by_id(
    db: Session,
    game_id: int,
):
    """Get a game using the internal database ID."""

    return (
        db.query(Game)
        .filter(
            Game.id == game_id
        )
        .first()
    )


def get_all_games(db: Session):
    """Return all games."""

    return (
        db.query(Game)
        .order_by(
            Game.game_date.desc()
        )
        .all()
    )


def get_unposted_games(db: Session):
    """
    Return games that:

    1. Are FINAL
    2. Have not been posted
    """

    return (
        db.query(Game)
        .filter(
            Game.posted.is_(False)
        )
        .filter(
            Game.status == "STATUS_FINAL"
        )
        .order_by(
            Game.game_date.asc()
        )
        .all()
    )


def mark_game_posted(
    db: Session,
    game_id: int,
):
    """Mark a game as successfully posted."""

    game = (
        db.query(Game)
        .filter(
            Game.id == game_id
        )
        .first()
    )

    if not game:
        return None

    game.posted = True
    game.updated_at = utc_now()

    db.commit()
    db.refresh(game)

    return game


# ============================================================
# TOP PLAYER FUNCTIONS
# ============================================================

def save_top_players(
    db: Session,
    game_id: int,
    top_players: list,
):
    """
    Save the top two players for a game.

    Players are expected to already be sorted by:

        Points + Assists + Rebounds

    Example player:

    {
        "name": "Player Name",
        "team": "Indiana Fever",
        "points": 28,
        "assists": 7,
        "rebounds": 11,
        "pra": 46
    }
    """

    game = (
        db.query(Game)
        .filter(
            Game.id == game_id
        )
        .first()
    )

    if not game:
        return None

    # --------------------------------------------------------
    # PLAYER 1
    # --------------------------------------------------------

    if len(top_players) >= 1:

        player_1 = top_players[0]

        game.top_player_1_name = player_1["name"]

        game.top_player_1_points = player_1["points"]

        game.top_player_1_assists = player_1["assists"]

        game.top_player_1_rebounds = player_1["rebounds"]

    # --------------------------------------------------------
    # PLAYER 2
    # --------------------------------------------------------

    if len(top_players) >= 2:

        player_2 = top_players[1]

        game.top_player_2_name = player_2["name"]

        game.top_player_2_points = player_2["points"]

        game.top_player_2_assists = player_2["assists"]

        game.top_player_2_rebounds = player_2["rebounds"]

    game.updated_at = utc_now()

    db.commit()
    db.refresh(game)

    return game


# ============================================================
# TWEET FUNCTIONS
# ============================================================

def save_tweet(
    db: Session,
    game_id: int,
    tweet_text: str,
    tweet_id: str = None,
    tweet_type: str = "final_score",
    status: str = "posted",
):
    """Save a tweet record."""

    tweet = Tweet(
        game_id=game_id,
        tweet_id=tweet_id,
        tweet_type=tweet_type,
        tweet_text=tweet_text,
        status=status,
        created_at=utc_now(),
        posted_at=(
            utc_now()
            if status == "posted"
            else None
        ),
    )

    db.add(tweet)
    db.commit()
    db.refresh(tweet)

    return tweet


def get_tweet_by_id(
    db: Session,
    tweet_id: str,
):
    """Get a tweet using its X/Twitter ID."""

    return (
        db.query(Tweet)
        .filter(
            Tweet.tweet_id == tweet_id
        )
        .first()
    )


def get_tweets_for_game(
    db: Session,
    game_id: int,
):
    """Get all tweets associated with a game."""

    return (
        db.query(Tweet)
        .filter(
            Tweet.game_id == game_id
        )
        .order_by(
            Tweet.created_at.desc()
        )
        .all()
    )


def get_all_tweets(db: Session):
    """Return all tweets."""

    return (
        db.query(Tweet)
        .order_by(
            Tweet.created_at.desc()
        )
        .all()
    )
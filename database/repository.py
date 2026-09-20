from datetime import datetime

from database.models import (
    Game,
    Tweet,
    BotLog,
)


# =========================================================
# GAME FUNCTIONS
# =========================================================

def save_game(session, game):

    existing_game = (
        session.query(Game)
        .filter(
            Game.espn_game_id == game.espn_game_id
        )
        .first()
    )

    if existing_game:

        existing_game.sport = game.sport
        existing_game.league = game.league
        existing_game.game_date = game.game_date
        existing_game.away_team = game.away_team
        existing_game.home_team = game.home_team
        existing_game.away_score = game.away_score
        existing_game.home_score = game.home_score
        existing_game.status = game.status

        # IMPORTANT:
        # Do not change posted here.
        #
        # Once a game has been posted,
        # an ESPN refresh must not reset it
        # back to False.

        existing_game.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(existing_game)

        return existing_game

    # New game

    if game.created_at is None:
        game.created_at = datetime.utcnow()

    if game.updated_at is None:
        game.updated_at = datetime.utcnow()

    if game.posted is None:
        game.posted = False

    session.add(game)

    session.commit()

    session.refresh(game)

    return game


def game_exists(
    session,
    espn_game_id
):

    return (
        session.query(Game)
        .filter(
            Game.espn_game_id == espn_game_id
        )
        .first()
        is not None
    )


def get_game(
    session,
    espn_game_id
):

    return (
        session.query(Game)
        .filter(
            Game.espn_game_id == espn_game_id
        )
        .first()
    )

def get_all_games(session):
    """
    Return all games stored in the database.
    """
    return (
        session.query(Game)
        .order_by(Game.game_date)
        .all()
    )

def get_completed_games(session):

    return (
        session.query(Game)
        .filter(
            Game.status == "STATUS_FINAL"
        )
        .order_by(
            Game.game_date
        )
        .all()
    )


def get_unposted_games(session):

    return (
        session.query(Game)
        .filter(
            Game.status == "STATUS_FINAL"
        )
        .filter(
            Game.posted.is_(False)
        )
        .order_by(
            Game.game_date
        )
        .all()
    )


def mark_game_posted(
    session,
    espn_game_id
):

    game = get_game(
        session,
        espn_game_id
    )

    if game is None:
        return False

    game.posted = True
    game.updated_at = datetime.utcnow()

    session.commit()

    return True


# =========================================================
# TWEET FUNCTIONS
# =========================================================

def save_tweet(
    session,
    game_id,
    tweet_id,
    tweet_type,
    tweet_text,
    status="posted"
):

    existing_tweet = get_tweet_by_game(
        session,
        game_id
    )

    if existing_tweet:

        return existing_tweet

    tweet = Tweet(

        game_id=game_id,

        tweet_id=tweet_id,

        tweet_type=tweet_type,

        tweet_text=tweet_text,

        status=status,

        posted_at=(
            datetime.utcnow()
            if status == "posted"
            else None
        )
    )

    session.add(tweet)

    session.commit()

    session.refresh(tweet)

    return tweet


def get_tweet_by_game(
    session,
    game_id
):

    return (
        session.query(Tweet)
        .filter(
            Tweet.game_id == str(game_id)
        )
        .first()
    )


def get_tweet_by_id(
    session,
    tweet_id
):

    return (
        session.query(Tweet)
        .filter(
            Tweet.tweet_id == tweet_id
        )
        .first()
    )


# =========================================================
# BOT LOG FUNCTIONS
# =========================================================

def save_bot_log(
    session,
    level,
    message
):

    log = BotLog(

        level=level,

        message=message

    )

    session.add(log)

    session.commit()

    session.refresh(log)

    return log
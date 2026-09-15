from sqlalchemy.orm import Session

from database.models import Game


def save_game(db: Session, game_data: dict):

    existing_game = (
        db.query(Game)
        .filter(
            Game.espn_game_id
            == game_data["espn_game_id"]
        )
        .first()
    )

    if existing_game:

        existing_game.game_date = game_data["game_date"]
        existing_game.away_team = game_data["away_team"]
        existing_game.home_team = game_data["home_team"]
        existing_game.away_score = game_data["away_score"]
        existing_game.home_score = game_data["home_score"]
        existing_game.status = game_data["status"]

        db.commit()
        db.refresh(existing_game)

        return existing_game

    new_game = Game(
        espn_game_id=game_data["espn_game_id"],
        game_date=game_data["game_date"],
        away_team=game_data["away_team"],
        home_team=game_data["home_team"],
        away_score=game_data["away_score"],
        home_score=game_data["home_score"],
        status=game_data["status"],
    )

    db.add(new_game)

    db.commit()
    db.refresh(new_game)

    return new_game


def get_all_games(db: Session):

    return (
        db.query(Game)
        .order_by(Game.game_date)
        .all()
    )

def get_completed_games(db: Session):

    return (
        db.query(Game)
        .filter(
            Game.status == "STATUS_FINAL"
        )
        .order_by(Game.game_date)
        .all()
    )
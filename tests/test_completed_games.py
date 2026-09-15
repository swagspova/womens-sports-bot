from database.db import SessionLocal
from database.repository import get_completed_games


def main():

    print("=" * 60)
    print("COMPLETED WNBA GAMES")
    print("=" * 60)

    db = SessionLocal()

    try:

        games = get_completed_games(db)

        print()
        print(
            f"Completed games: {len(games)}"
        )

        for game in games:

            print()
            print(
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team}"
            )

            print(
                f"ESPN ID: {game.espn_game_id}"
            )

    finally:

        db.close()


if __name__ == "__main__":
    main()
from database.db import SessionLocal
from database.init_db import init_db
from database.repository import save_game, get_all_games

from bot.api.espn import ESPNWNBAClient


def main():

    print()
    print("=" * 60)
    print("ESPN → DATABASE TEST")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Initialize database
    # --------------------------------------------------

    init_db()

    # --------------------------------------------------
    # 2. Create ESPN client
    # --------------------------------------------------

    client = ESPNWNBAClient()

    print()
    print("Fetching WNBA games from ESPN...")

    # --------------------------------------------------
    # 3. Retrieve games
    # --------------------------------------------------

    games = client.get_games()

    print()
    print(
        f"Games received from ESPN: {len(games)}"
    )

    if not games:
        print()
        print("No games returned by ESPN.")
        print("Try a date that contains WNBA games.")
        return

    # --------------------------------------------------
    # 4. Open database session
    # --------------------------------------------------

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # 5. Save games
        # --------------------------------------------------

        for game_data in games:

            print()
            print("Game:")

            print(
                f"{game_data['away_team']} "
                f"{game_data['away_score']} - "
                f"{game_data['home_score']} "
                f"{game_data['home_team']}"
            )

            print(
                f"ESPN ID: "
                f"{game_data['espn_game_id']}"
            )

            print("Saving game to database...")

            game = save_game(
                db,
                game_data
            )

            print(
                f"Game saved successfully. "
                f"Database ID: {game.id}"
            )

        # --------------------------------------------------
        # 6. Read games back
        # --------------------------------------------------

        print()
        print("=" * 60)
        print("DATABASE VERIFICATION")
        print("=" * 60)

        saved_games = get_all_games(db)

        print()
        print(
            f"Games in database: "
            f"{len(saved_games)}"
        )

        for game in saved_games:

            print()
            print(
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team}"
            )

            print(
                f"ESPN ID: "
                f"{game.espn_game_id}"
            )

            print(
                f"Status: "
                f"{game.status}"
            )

    finally:

        db.close()

    print()
    print("=" * 60)
    print("DAY 3 COMPLETE")
    print("=" * 60)

    print()
    print("✓ ESPN API working")
    print("✓ ESPN data parsed")
    print("✓ Database connection working")
    print("✓ Games saved")
    print("✓ Games retrieved")
    print("✓ ESPN → Database pipeline working")

    print()


if __name__ == "__main__":
    main()
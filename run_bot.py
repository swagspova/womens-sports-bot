import config

from database import init_db
from database.db import get_session
from database.repository import save_game

from bot.api.espn import get_wnba_games
from bot.processor import GameProcessor
from bot.twitter_client import TwitterClient


def main():

    print("=" * 70)
    print("WOMEN'S SPORTS BOT")
    print("=" * 70)

    print("\nStarting hourly bot run...")

    # ============================================================
    # 1. INITIALIZE DATABASE
    # ============================================================

    init_db()

    # ============================================================
    # 2. DATABASE SESSION
    # ============================================================

    db = get_session()

    try:

        # ========================================================
        # 3. FETCH ESPN GAMES
        # ========================================================

        print("\nFetching WNBA games from ESPN...")

        games = get_wnba_games()

        print(f"Fetched {len(games)} games from ESPN.")

        # ========================================================
        # 4. SAVE / UPDATE GAMES IN DATABASE
        # ========================================================

        print("\nSaving games to database...")

        saved_count = 0

        for game_data in games:

            saved_game = save_game(
                db=db,
                game_data=game_data
            )

            saved_count += 1

            print(
                f"Saved: "
                f"{saved_game.away_team} "
                f"vs "
                f"{saved_game.home_team} "
                f"(ESPN ID: {saved_game.espn_game_id})"
            )

        print(
            f"\nSaved/updated {saved_count} game(s) "
            "in database."
        )

        # ========================================================
        # 5. TWITTER CLIENT
        # ========================================================

        twitter_client = TwitterClient()

        # ========================================================
        # 6. GAME PROCESSOR
        # ========================================================

        processor = GameProcessor(
            db=db,
            twitter_client=twitter_client
        )

        # ========================================================
        # 7. PROCESS UNPOSTED FINAL GAMES
        # ========================================================

        result = processor.process_unposted_games()

        # ========================================================
        # 8. FINAL SUMMARY
        # ========================================================

        print("\n" + "=" * 70)
        print("RUN SUMMARY")
        print("=" * 70)

        print(f"Games fetched:    {len(games)}")
        print(f"Games saved:      {saved_count}")
        print(
            f"Games processed:  "
            f"{result.get('processed', 0)}"
        )
        print(
            f"Games failed:     "
            f"{result.get('failed', 0)}"
        )

        print("=" * 70)

    finally:

        db.close()


if __name__ == "__main__":
    main()
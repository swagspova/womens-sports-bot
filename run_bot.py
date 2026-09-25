from database import init_db
from database.db import get_session

from bot.api.espn import get_wnba_games
from bot.processor import GameProcessor
from bot.twitter_client import TwitterClient


def main():

    print("=" * 70)
    print("WOMEN'S SPORTS BOT")
    print("=" * 70)

    print("Starting hourly bot run...")

    # Make sure tables exist
    init_db()

    # Database session
    db = get_session()

    try:

        # --------------------------------------------------
        # 1. Fetch ESPN games
        # --------------------------------------------------

        print("\nFetching WNBA games from ESPN...")

        games = get_wnba_games()

        print(
            f"Fetched {len(games)} games from ESPN."
        )

        # --------------------------------------------------
        # 2. Twitter client
        # --------------------------------------------------

        twitter_client = TwitterClient()

        # --------------------------------------------------
        # 3. Processor
        # --------------------------------------------------

        processor = GameProcessor(
            db=db,
            twitter_client=twitter_client
        )

        # --------------------------------------------------
        # 4. Process games
        # --------------------------------------------------

        processed = 0
        posted = 0
        skipped = 0
        errors = 0

        for game in games:

            try:

                result = processor.process_game(
                    game
                )

                processed += 1

                if result == "posted":
                    posted += 1

                elif result == "skipped":
                    skipped += 1

            except Exception as e:

                errors += 1

                print(
                    "\nERROR processing game:"
                )

                print(
                    f"{type(e).__name__}: {e}"
                )

                print(
                    "Game will remain unposted."
                )

        # --------------------------------------------------
        # 5. Summary
        # --------------------------------------------------

        print("\n" + "=" * 70)
        print("RUN SUMMARY")
        print("=" * 70)

        print(f"Games fetched:    {len(games)}")
        print(f"Games processed:  {processed}")
        print(f"Tweets posted:    {posted}")
        print(f"Games skipped:    {skipped}")
        print(f"Errors:           {errors}")

        print("=" * 70)

    finally:

        db.close()


if __name__ == "__main__":
    main()
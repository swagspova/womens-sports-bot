from database import (
    init_db,
    get_session,
)

from database.repository import (
    get_unposted_games,
)

from bot.twitter_client import TwitterClient

from bot.processor import GameProcessor

from scheduler.scheduler import Scheduler


def main():

    print()
    print("=" * 70)
    print("FULL PIPELINE TEST")
    print("=" * 70)

    init_db()

    db = get_session()

    try:

        twitter = TwitterClient()

        processor = GameProcessor(
            db=db,
            twitter_client=twitter,
        )

        scheduler = Scheduler(
            db=db,
            processor=processor,
            interval_seconds=120,
        )

        scheduler.run_once()

        games = get_unposted_games(
            db
        )

        print()
        print(
            f"Remaining unposted final games: "
            f"{len(games)}"
        )

        print()
        print(
            "FULL PIPELINE TEST COMPLETED"
        )

    finally:

        db.close()


if __name__ == "__main__":
    main()
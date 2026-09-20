from database import init_db

from bot.tweet_service import TweetService


def main():

    print()
    print("=" * 60)
    print("WOMEN'S SPORTS BOT")
    print("=" * 60)

    print()
    print("Initializing database...")

    init_db()

    print("Database initialized.")

    print()
    print("Starting tweet service...")

    service = TweetService()

    results = service.process_unposted_games()

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    if not results:

        print("No games processed.")

    else:

        for result in results:

            print(result)

    print()
    print("Application finished.")


if __name__ == "__main__":

    main()
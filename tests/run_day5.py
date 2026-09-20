from bot.tweet_service import (
    process_unposted_games,
)


def main():

    print("\n")
    print("=" * 60)
    print("DAY 5 — FINAL SCORE TWEET SERVICE")
    print("=" * 60)

    results = process_unposted_games()

    print("\nFinal Results:")

    for result in results:

        print(result)

    print()
    print("=" * 60)
    print("DAY 5 COMPLETE")
    print("=" * 60)


if __name__ == "__main__":

    main()
from database import (
    get_session,
    get_completed_games,
)

from bot.tweet_builder import (
    build_final_score_tweet,
)


def main():

    print("\n")
    print("=" * 60)
    print("TWEET BUILDER TEST")
    print("=" * 60)

    session = get_session()

    try:

        games = get_completed_games(
            session
        )

        print(
            f"\nCompleted games: "
            f"{len(games)}"
        )

        for game in games:

            print("\n")
            print("-" * 60)

            print(
                f"Game: "
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team}"
            )

            tweet = build_final_score_tweet(
                game
            )

            print("\nGenerated Tweet:")
            print("-" * 60)

            print(tweet.text)

            print("-" * 60)

            print(
                f"Characters: "
                f"{len(tweet.text)}"
            )

            print(
                f"Game ID: "
                f"{tweet.game_id}"
            )

            print("-" * 60)

    finally:

        session.close()


if __name__ == "__main__":

    main()
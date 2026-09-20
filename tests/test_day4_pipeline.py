from database.db import SessionLocal
from database.repository import get_completed_games
from bot.tweet_builder import build_final_score_tweet
from bot.twitter_client import TwitterClient


def main():
    print("\n")
    print("=" * 70)
    print("DAY 4 PIPELINE TEST")
    print("=" * 70)

    session = SessionLocal()

    try:
        print("\n1. Reading completed games from database...")

        games = get_completed_games(session)

        print(f"Completed games found: {len(games)}")

        if not games:
            print("\nNo completed games available.")
            return

        twitter_client = TwitterClient()

        for game in games:

            print("\n" + "=" * 70)

            print("2. GAME")
            print(
                f"{game.away_team} {game.away_score} - "
                f"{game.home_score} {game.home_team}"
            )

            print(f"ESPN ID: {game.espn_game_id}")
            print(f"Status: {game.status}")

            print("\n3. BUILDING TWEET...")

            tweet = build_final_score_tweet(game)

            print("\nGenerated Tweet:")
            print("-" * 50)
            print(tweet.text)
            print("-" * 50)

            print(f"Game ID: {tweet.game_id}")
            print(f"Characters: {len(tweet.text)}")

            print("\n4. SENDING TO TWITTER CLIENT...")

            result = twitter_client.post_tweet(tweet.text)

            print("\nTwitter Client Result:")
            print(result)

    finally:
        session.close()

    print("\n")
    print("=" * 70)
    print("DAY 4 PIPELINE TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
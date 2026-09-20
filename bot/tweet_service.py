from database import (
    get_session,
    get_unposted_games,
    get_tweet_by_game,
    save_tweet,
    mark_game_posted,
)

from bot.tweet_builder import (
    build_final_score_tweet,
)

from bot.twitter_client import (
    TwitterClient,
)


def process_unposted_games():

    session = get_session()

    twitter = TwitterClient()

    results = []

    try:

        games = get_unposted_games(
            session
        )

        print()
        print("=" * 60)
        print("TWEET SERVICE")
        print("=" * 60)

        print(
            f"\nUnposted completed games: "
            f"{len(games)}"
        )

        for game in games:

            print()
            print("-" * 60)

            print(
                f"Processing: "
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team}"
            )

            # -------------------------------------------------
            # DUPLICATE CHECK
            # -------------------------------------------------

            existing_tweet = get_tweet_by_game(
                session,
                game.espn_game_id
            )

            if existing_tweet:

                print(
                    "Tweet already exists. "
                    "Skipping."
                )

                results.append({
                    "game_id": game.espn_game_id,
                    "status": "already_exists"
                })

                continue

            # -------------------------------------------------
            # BUILD TWEET
            # -------------------------------------------------

            tweet = build_final_score_tweet(
                game
            )

            print(
                "\nGenerated tweet:"
            )

            print(tweet.text)

            # -------------------------------------------------
            # POST TWEET
            # -------------------------------------------------

            result = twitter.post_tweet(
                tweet.text
            )

            if result["dry_run"]:

                print(
                    "\nDRY RUN:"
                    " database will not be modified."
                )

                results.append({
                    "game_id": game.espn_game_id,
                    "status": "dry_run"
                })

                continue


            saved_tweet = save_tweet(

                session=session,

                game_id=game.espn_game_id,

                tweet_id=result["tweet_id"],

                tweet_type="final_score",

                tweet_text=tweet.text,

                status="posted"

            )


            mark_game_posted(
                session,
                game.espn_game_id
            )


            print(
                "\nGame marked as posted."
            )


            results.append({
                "game_id": game.espn_game_id,
                "status": "posted",
                "tweet_id": result["tweet_id"]
            })

            results.append({
                "game_id": game.espn_game_id,
                "status": "posted",
                "tweet_id": result["tweet_id"]
            })

        print()
        print("=" * 60)
        print("TWEET SERVICE COMPLETE")
        print("=" * 60)

        return results

    finally:

        session.close()
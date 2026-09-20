from database.db import get_session

from database.repository import (
    get_unposted_games,
    mark_game_posted,
)

from bot.tweet_builder import build_final_score_tweet


class GameProcessor:

    def __init__(self, dry_run=False):

        self.dry_run = dry_run

    # =====================================================
    # PROCESS COMPLETED GAMES
    # =====================================================

    def process_completed_games(self):

        print()
        print("=" * 60)
        print("PROCESSING COMPLETED GAMES")
        print("=" * 60)

        db = get_session()

        try:

            games = get_unposted_games(db)

            print(
                f"Unposted completed games: {len(games)}"
            )

            processed_count = 0

            for game in games:

                print()
                print("-" * 60)

                print(
                    f"Game ID: {game.espn_game_id}"
                )

                print(
                    f"{game.away_team} "
                    f"{game.away_score} - "
                    f"{game.home_score} "
                    f"{game.home_team}"
                )

                # -----------------------------------------
                # BUILD TWEET
                # -----------------------------------------

                tweet = build_final_score_tweet(
                    game
                )

                print()
                print("Generated tweet:")
                print(tweet.text)

                print()
                print(
                    f"Tweet game ID: "
                    f"{tweet.game_id}"
                )

                # -----------------------------------------
                # DRY RUN
                # -----------------------------------------

                if self.dry_run:

                    print()
                    print(
                        "DRY RUN: Tweet NOT published."
                    )

                    processed_count += 1

                    continue

                # -----------------------------------------
                # TWITTER PUBLISHING
                # -----------------------------------------

                print()
                print(
                    "Twitter publishing is not enabled yet."
                )

                # IMPORTANT:
                #
                # Do NOT mark the game as posted here.
                #
                # mark_game_posted() should only happen
                # after Twitter confirms successful
                # publication.

            print()
            print("=" * 60)
            print("PROCESSING COMPLETE")
            print("=" * 60)

            print(
                f"Games processed: {processed_count}"
            )

            return processed_count

        finally:

            db.close()

            print()
            print("Database session closed.")
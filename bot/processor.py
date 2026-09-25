from database.repository import (
    get_unposted_games,
    save_top_players,
    save_tweet,
    mark_game_posted,
)

from bot.api.espn import (
    get_top_two_players,
)

from bot.tweet_builder import (
    build_final_score_tweet,
)


class GameProcessor:
    """
    Processes final WNBA games that have not yet been posted.

    Expected usage from run_bot.py:

        processor = GameProcessor(
            db=db,
            twitter_client=twitter_client,
        )

        processor.process_unposted_games()
    """

    def __init__(
        self,
        db,
        twitter_client,
    ):
        """
        Initialize the game processor.

        Parameters
        ----------
        db:
            SQLAlchemy database session.

        twitter_client:
            Existing TwitterClient instance created by run_bot.py.
        """

        self.db = db
        self.twitter_client = twitter_client

    # ============================================================
    # PROCESS UNPOSTED GAMES
    # ============================================================

    def process_unposted_games(self):
        """
        Process all final games that have not been posted.

        Flow:

            SQLite
                ↓
            Final + unposted games
                ↓
            ESPN player statistics
                ↓
            Top 2 players by PTS + AST + REB
                ↓
            Save player statistics
                ↓
            Build tweet
                ↓
            Twitter/X
                ↓
            Save tweet
                ↓
            Mark game posted
        """

        processed_count = 0
        failed_count = 0

        games = get_unposted_games(
            self.db
        )

        print(
            f"\nFound {len(games)} "
            f"unposted final game(s).\n"
        )

        for game in games:

            print(
                "=" * 70
            )

            print(
                f"Processing: "
                f"{game.away_team} "
                f"vs "
                f"{game.home_team}"
            )

            print(
                f"ESPN ID: "
                f"{game.espn_game_id}"
            )

            try:

                # ====================================================
                # STEP 1
                # GET TOP TWO PLAYERS
                # ====================================================

                top_players = get_top_two_players(
                    game.espn_game_id
                )

                if not top_players:

                    raise ValueError(
                        "No player statistics were "
                        "returned by ESPN."
                    )

                print(
                    "\nTop performers:"
                )

                for index, player in enumerate(
                    top_players,
                    start=1,
                ):

                    print(
                        f"{index}. "
                        f"{player['name']} - "
                        f"{player['points']} PTS | "
                        f"{player['assists']} AST | "
                        f"{player['rebounds']} REB "
                        f"(PRA: {player['pra']})"
                    )

                # ====================================================
                # STEP 2
                # SAVE TOP PLAYERS
                # ====================================================

                save_top_players(
                    db=self.db,
                    game_id=game.id,
                    top_players=top_players,
                )

                # Refresh the SQLAlchemy object so the tweet
                # builder sees the newly saved player fields.

                self.db.refresh(game)

                # ====================================================
                # STEP 3
                # BUILD TWEET
                # ====================================================

                tweet = build_final_score_tweet(
                    game
                )

                print(
                    "\nGenerated tweet:"
                )

                print(
                    "-" * 70
                )

                print(
                    tweet.text
                )

                print(
                    "-" * 70
                )

                print(
                    f"Characters: "
                    f"{len(tweet.text)}/280"
                )

                # ====================================================
                # STEP 4
                # POST TWEET
                # ====================================================

                result = self.twitter_client.post_tweet(
                    tweet.text
                )

                # ====================================================
                # STEP 5
                # CHECK RESULT
                # ====================================================

                if not result.get("success"):

                    print(
                        "\nTweet failed."
                    )

                    print(
                        "Game will remain unposted."
                    )

                    failed_count += 1

                    continue

                # ====================================================
                # DRY RUN
                # ====================================================

                if result.get("dry_run"):

                    print(
                        "\nDRY RUN completed."
                    )

                    print(
                        "Game remains unposted."
                    )

                    processed_count += 1

                    continue

                # ====================================================
                # REAL X POST
                # ====================================================

                tweet_id = result.get(
                    "tweet_id"
                )

                if not tweet_id:

                    print(
                        "\nTweet succeeded but "
                        "no tweet ID was returned."
                    )

                    print(
                        "Game will remain unposted."
                    )

                    failed_count += 1

                    continue

                # ====================================================
                # STEP 6
                # SAVE TWEET
                # ====================================================

                save_tweet(
                    db=self.db,
                    game_id=game.id,
                    tweet_text=tweet.text,
                    tweet_id=tweet_id,
                    tweet_type="final_score",
                    status="posted",
                )

                # ====================================================
                # STEP 7
                # MARK GAME POSTED
                # ====================================================

                mark_game_posted(
                    db=self.db,
                    game_id=game.id,
                )

                print(
                    "\nTweet posted successfully."
                )

                print(
                    f"Tweet ID: {tweet_id}"
                )

                processed_count += 1

            except Exception as error:

                print(
                    "\nERROR processing game:"
                )

                print(
                    f"{type(error).__name__}: "
                    f"{error}"
                )

                print(
                    "Game will remain unposted."
                )

                failed_count += 1

        # ============================================================
        # SUMMARY
        # ============================================================

        print(
            "\n" + "=" * 70
        )

        print(
            "PROCESSING SUMMARY"
        )

        print(
            "=" * 70
        )

        print(
            f"Processed: {processed_count}"
        )

        print(
            f"Failed:    {failed_count}"
        )

        print(
            "=" * 70
        )

        return {
            "processed": processed_count,
            "failed": failed_count,
        }
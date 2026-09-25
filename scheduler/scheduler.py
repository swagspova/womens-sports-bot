import time
from datetime import datetime

from bot.api.espn import get_wnba_games
from database.repository import save_game


class Scheduler:

    def __init__(
        self,
        db,
        processor,
        interval_seconds=120
    ):

        self.db = db
        self.processor = processor
        self.interval_seconds = (
            interval_seconds
        )

        self.running = True


    def fetch_and_save_games(self):

        print()
        print(
            "Fetching WNBA games from ESPN..."
        )

        games = get_wnba_games()

        print(
            f"Games received from ESPN: "
            f"{len(games)}"
        )

        for game_data in games:

            game = save_game(
                self.db,
                game_data
            )

            print(
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team} | "
                f"{game.status}"
            )

        return games


    def run_once(self):

        print()
        print("=" * 70)
        print(
            "SCHEDULER CYCLE"
        )
        print(
            datetime.now().isoformat()
        )
        print("=" * 70)

        try:

            self.fetch_and_save_games()

            result = (
                self.processor
                .process_unposted_games()
            )

            print()
            print(
                f"Processed: "
                f"{result['processed']}"
            )

            print(
                f"Failed: "
                f"{result['failed']}"
            )

            return result

        except Exception as exc:

            print()
            print(
                f"Scheduler error: {exc}"
            )

            return {
                "processed": 0,
                "failed": 1,
            }


    def run_forever(self):

        print()
        print(
            "Women's Sports Bot"
        )

        print(
            f"Polling every "
            f"{self.interval_seconds} seconds"
        )

        print(
            "Press Ctrl+C to stop."
        )

        while self.running:

            self.run_once()

            print()
            print(
                f"Sleeping for "
                f"{self.interval_seconds} seconds..."
            )

            try:

                time.sleep(
                    self.interval_seconds
                )

            except KeyboardInterrupt:

                self.running = False

                print()
                print(
                    "Bot stopped."
                )
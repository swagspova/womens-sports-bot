import time
import logging

from database.db import get_session
from database.models import Game

from database.repository import (
    save_game,
    get_unposted_games,
    mark_game_posted,
)

from bot.api.espn import get_wnba_games


logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self, interval=300, dry_run=False):
        self.interval = interval
        self.dry_run = dry_run
        self.running = False

    # =====================================================
    # CONVERT ESPN EVENT TO GAME
    # =====================================================

    def convert_event_to_game(self, event):

        from datetime import datetime

        competitions = event.get(
            "competitions",
            []
        )

        if not competitions:
            return None

        competition = competitions[0]

        competitors = competition.get(
            "competitors",
            []
        )

        if len(competitors) < 2:
            return None

        away_team = None
        home_team = None

        away_score = None
        home_score = None

        for competitor in competitors:

            team_name = (
                competitor
                .get("team", {})
                .get("displayName")
            )

            score = competitor.get("score")

            if score is not None:
                score = int(score)

            if competitor.get("homeAway") == "away":

                away_team = team_name
                away_score = score

            elif competitor.get("homeAway") == "home":

                home_team = team_name
                home_score = score

        status = (
            event
            .get("status", {})
            .get("type", {})
            .get("name")
        )

        game_date_string = event.get("date")

        game_date = None

        if game_date_string:

            game_date = datetime.fromisoformat(
                game_date_string.replace(
                    "Z",
                    "+00:00"
                )
            )

        game = Game(
            espn_game_id=str(
                event.get("id")
            ),
            sport="basketball",
            league="WNBA",
            game_date=game_date,
            away_team=away_team,
            home_team=home_team,
            away_score=away_score,
            home_score=home_score,
            status=status,
            posted=False,
        )

        return game

    # =====================================================
    # FETCH AND SAVE GAMES
    # =====================================================

    def update_games(self):

        logger.info(
            "Fetching games from ESPN..."
        )

        events = get_wnba_games()

        logger.info(
            "Games received from ESPN: %s",
            len(events)
        )

        db = get_session()

        try:

            saved_count = 0

            for event in events:

                game = self.convert_event_to_game(
                    event
                )

                if game is None:

                    logger.warning(
                        "Skipping invalid ESPN event."
                    )

                    continue

                saved_game = save_game(
                    db,
                    game
                )

                saved_count += 1

                logger.info(
                    "Game saved: %s %s - %s %s | %s",
                    saved_game.away_team,
                    saved_game.away_score,
                    saved_game.home_score,
                    saved_game.home_team,
                    saved_game.status
                )

            logger.info(
                "Games processed: %s",
                saved_count
            )

        finally:

            db.close()

    # =====================================================
    # PROCESS COMPLETED GAMES
    # =====================================================

    def process_completed_games(self):

        db = get_session()

        try:

            games = get_unposted_games(db)

            logger.info(
                "Unposted completed games: %s",
                len(games)
            )

            for game in games:

                tweet_text = (
                    f"🏀 WNBA FINAL\n\n"
                    f"{game.away_team} "
                    f"{game.away_score} - "
                    f"{game.home_score} "
                    f"{game.home_team}"
                )

                logger.info(
                    "Tweet generated: %s",
                    tweet_text
                )

                # -----------------------------------------
                # DRY RUN
                # -----------------------------------------

                if self.dry_run:

                    print(
                        "\nDRY RUN - Tweet:"
                    )

                    print(
                        tweet_text
                    )

                    continue

                # -----------------------------------------
                # PUBLISH
                # -----------------------------------------

                # Twitter publishing will be connected
                # after the scheduler/database flow is
                # confirmed working.

                logger.info(
                    "Twitter publishing is not enabled yet."
                )

        finally:

            db.close()

    # =====================================================
    # RUN ONE CYCLE
    # =====================================================

    def run_once(self):

        logger.info(
            "Starting scheduler cycle..."
        )

        self.update_games()

        self.process_completed_games()

        logger.info(
            "Scheduler cycle complete."
        )

    # =====================================================
    # CONTINUOUS RUN
    # =====================================================

    def run(self):

        self.running = True

        logger.info(
            "Scheduler started."
        )

        logger.info(
            "Polling interval: %s seconds",
            self.interval
        )

        try:

            while self.running:

                self.run_once()

                if not self.running:
                    break

                logger.info(
                    "Sleeping for %s seconds...",
                    self.interval
                )

                time.sleep(
                    self.interval
                )

        except KeyboardInterrupt:

            logger.info(
                "Keyboard interrupt received."
            )

        finally:

            self.running = False

            logger.info(
                "Scheduler stopped."
            )

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        self.running = False
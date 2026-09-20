from datetime import datetime

from database.db import get_session

from database.repository import (
    save_game,
    get_all_games,
)

from bot.api.espn import get_wnba_games


def main():

    print("\n")
    print("=" * 70)
    print("ESPN → DATABASE TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Create database session
    # ---------------------------------------------------------

    db = get_session()

    print("\nDatabase session created.")

    try:

        # -----------------------------------------------------
        # 2. Get games from ESPN
        # -----------------------------------------------------

        print("\nFetching games from ESPN...")

        events = get_wnba_games()

        print(f"Games received from ESPN: {len(events)}")

        # -----------------------------------------------------
        # 3. Save games
        # -----------------------------------------------------

        print("\nSaving games to database...")

        saved_count = 0

        for event in events:

            print("\nProcessing ESPN event...")

            print(
                f"ESPN ID: "
                f"{event.get('id')}"
            )

            # -------------------------------------------------
            # IMPORTANT
            #
            # Your current repository.save_game() expects
            # a SQLAlchemy Game object:
            #
            #     save_game(session, game)
            #
            # Therefore we need to convert the ESPN event
            # into the Game model before saving.
            # -------------------------------------------------

            from database.models import Game

            competitions = event.get(
                "competitions",
                []
            )

            if not competitions:
                print("No competition data found. Skipping.")
                continue

            competition = competitions[0]

            competitors = competition.get(
                "competitors",
                []
            )

            if len(competitors) < 2:
                print("Not enough competitors. Skipping.")
                continue

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

                if competitor.get("homeAway") == "home":

                    home_team = team_name
                    home_score = score

                elif competitor.get("homeAway") == "away":

                    away_team = team_name
                    away_score = score

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
                    game_date_string.replace("Z", "+00:00")
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

            saved_game = save_game(
                db,
                game
            )

            saved_count += 1

            print(
                f"Saved: "
                f"{saved_game.away_team} "
                f"{saved_game.away_score} - "
                f"{saved_game.home_score} "
                f"{saved_game.home_team}"
            )

        # -----------------------------------------------------
        # 4. Retrieve all games
        # -----------------------------------------------------

        print("\n")
        print("=" * 70)
        print("DATABASE GAMES")
        print("=" * 70)

        saved_games = get_all_games(db)

        print(
            f"Total games in database: "
            f"{len(saved_games)}"
        )

        for game in saved_games:

            print(
                f"\n"
                f"ID: {game.espn_game_id}\n"
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team}\n"
                f"Status: {game.status}\n"
                f"Posted: {game.posted}"
            )

        # -----------------------------------------------------
        # 5. Summary
        # -----------------------------------------------------

        print("\n")
        print("=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        print(
            f"ESPN games received : {len(events)}"
        )

        print(
            f"Games processed     : {saved_count}"
        )

        print(
            f"Games in database   : {len(saved_games)}"
        )

        print("=" * 70)

    finally:

        db.close()

        print("\nDatabase session closed.")


if __name__ == "__main__":
    main()
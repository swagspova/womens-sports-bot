from database import (
    init_db,
    get_session,
    save_game,
    get_game,
    game_exists,
    mark_game_posted
)

from logger import log_info


def main():

    print("\n")
    print("=" * 60)
    print("DAY 2 STORAGE FLOW TEST")
    print("=" * 60)

    # --------------------------------------------------
    # STEP 1
    # --------------------------------------------------

    init_db()

    session = get_session()

    try:

        # --------------------------------------------------
        # STEP 2
        # Simulated ESPN game
        # --------------------------------------------------

        game_data = {

            "espn_game_id": "DAY2-001",

            "sport": "basketball",

            "league": "WNBA",

            "home_team": "Indiana Fever",

            "away_team": "Phoenix Mercury",

            "home_score": 92,

            "away_score": 88,

            "status": "final",

            "game_date": None,

            "posted": False

        }

        print("\nGame received.")

        # --------------------------------------------------
        # STEP 3
        # Check duplicate
        # --------------------------------------------------

        if game_exists(
            session,
            game_data["espn_game_id"]
        ):

            print(
                "Game already exists."
            )

        else:

            print(
                "Game does not exist."
            )

            # --------------------------------------------------
            # STEP 4
            # Save game
            # --------------------------------------------------

            game = save_game(
                session,
                game_data
            )

            print(
                f"Game saved: "
                f"{game.espn_game_id}"
            )

            log_info(
                f"Game saved: "
                f"{game.espn_game_id}"
            )

        # --------------------------------------------------
        # STEP 5
        # Retrieve game
        # --------------------------------------------------

        game = get_game(
            session,
            "DAY2-001"
        )

        print("\nStored game:")

        print(
            f"{game.away_team} "
            f"{game.away_score} - "
            f"{game.home_score} "
            f"{game.home_team}"
        )

        print(
            f"Posted: {game.posted}"
        )

        # --------------------------------------------------
        # STEP 6
        # Simulate successful tweet
        # --------------------------------------------------

        print(
            "\nSimulating successful tweet..."
        )

        mark_game_posted(
            session,
            "DAY2-001"
        )

        # --------------------------------------------------
        # STEP 7
        # Verify
        # --------------------------------------------------

        game = get_game(
            session,
            "DAY2-001"
        )

        print(
            f"Posted after tweet: "
            f"{game.posted}"
        )

        print("\nStorage flow successful.")

    finally:

        session.close()

    print("\n")
    print("=" * 60)
    print("DAY 2 STORAGE FLOW COMPLETE")
    print("=" * 60)
    print("\n")


if __name__ == "__main__":
    main()
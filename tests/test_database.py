from database import (
    init_db,
    get_session,
    save_game,
    game_exists,
    get_game,
    get_unposted_games,
    mark_game_posted
)


def main():

    print("\n")
    print("=" * 60)
    print("DATABASE TEST")
    print("=" * 60)

    # Initialize database
    init_db()

    # Open session
    session = get_session()

    try:

        test_game = {
            "espn_game_id": "TEST-001",
            "sport": "basketball",
            "league": "WNBA",
            "home_team": "New York Liberty",
            "away_team": "Chicago Sky",
            "home_score": 85,
            "away_score": 66,
            "status": "final",
            "game_date": None,
            "posted": False
        }

        print("\nSaving test game...")

        game = save_game(
            session,
            test_game
        )

        print(
            f"Game saved successfully: "
            f"{game.espn_game_id}"
        )

        print("\nChecking whether game exists...")

        exists = game_exists(
            session,
            "TEST-001"
        )

        print(
            f"Game exists: {exists}"
        )

        print("\nRetrieving game...")

        retrieved_game = get_game(
            session,
            "TEST-001"
        )

        print(
            f"Retrieved: "
            f"{retrieved_game.away_team} "
            f"{retrieved_game.away_score} - "
            f"{retrieved_game.home_score} "
            f"{retrieved_game.home_team}"
        )

        print("\nChecking unposted games...")

        unposted = get_unposted_games(
            session
        )

        print(
            f"Unposted games: {len(unposted)}"
        )

        print("\nMarking game as posted...")

        result = mark_game_posted(
            session,
            "TEST-001"
        )

        print(
            f"Marked posted: {result}"
        )

        retrieved_game = get_game(
            session,
            "TEST-001"
        )

        print(
            f"Posted status: "
            f"{retrieved_game.posted}"
        )

    finally:

        session.close()

    print("\n")
    print("=" * 60)
    print("DATABASE TEST COMPLETE")
    print("=" * 60)
    print("\n")


if __name__ == "__main__":
    main()
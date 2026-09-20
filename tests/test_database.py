from database import (
    init_db,
    get_session,
    get_completed_games,
    get_unposted_games,
)


def main():

    print("\n")
    print("=" * 60)
    print("DAY 5 DATABASE TEST")
    print("=" * 60)

    print("\nInitializing database...")

    init_db()

    print("Database initialized successfully.")

    session = get_session()

    try:

        completed_games = get_completed_games(
            session
        )

        unposted_games = get_unposted_games(
            session
        )

        print(
            f"\nCompleted games: "
            f"{len(completed_games)}"
        )

        print(
            f"Unposted completed games: "
            f"{len(unposted_games)}"
        )

        print("\nCompleted games:")

        for game in completed_games:

            print(
                f"{game.id}: "
                f"{game.away_team} "
                f"{game.away_score} - "
                f"{game.home_score} "
                f"{game.home_team} "
                f"| posted={game.posted}"
            )

        print("\n")
        print("=" * 60)
        print("DATABASE TEST PASSED")
        print("=" * 60)

    finally:

        session.close()


if __name__ == "__main__":
    main()
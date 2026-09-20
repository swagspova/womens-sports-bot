from database import (
    get_session,
    get_unposted_games,
)

from bot.tweet_service import (
    process_unposted_games,
)


def main():

    print("\n")
    print("=" * 60)
    print("DAY 5 TWEET SERVICE TEST")
    print("=" * 60)

    # ---------------------------------------------
    # BEFORE
    # ---------------------------------------------

    session = get_session()

    try:

        games_before = get_unposted_games(
            session
        )

        print(
            f"\nUnposted games BEFORE service: "
            f"{len(games_before)}"
        )

    finally:

        session.close()

    # ---------------------------------------------
    # RUN SERVICE
    # ---------------------------------------------

    results = process_unposted_games()

    print("\nResults:")

    for result in results:

        print(result)

    # ---------------------------------------------
    # AFTER
    # ---------------------------------------------

    session = get_session()

    try:

        games_after = get_unposted_games(
            session
        )

        print(
            f"\nUnposted games AFTER service: "
            f"{len(games_after)}"
        )

    finally:

        session.close()

    # ---------------------------------------------
    # VERIFY DRY RUN
    # ---------------------------------------------

    if len(games_before) != len(games_after):

        raise AssertionError(
            "Dry run changed the posted state."
        )

    print()
    print("=" * 60)
    print("DAY 5 TWEET SERVICE TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":

    main()
from bot.api.espn import get_wnba_games


def main():

    print("\n")
    print("=" * 60)
    print("ESPN WNBA API TEST")
    print("=" * 60)

    games = get_wnba_games()

    print(
        f"\nGames received from ESPN: "
        f"{len(games)}"
    )

    for event in games:

        print("\n")
        print("-" * 60)

        print(
            f"ESPN ID: "
            f"{event.get('id')}"
        )

        print(
            f"Name: "
            f"{event.get('name')}"
        )

        status = (
            event
            .get("status", {})
            .get("type", {})
            .get("name")
        )

        print(
            f"Status: {status}"
        )

    print("\nESPN TEST COMPLETE")


if __name__ == "__main__":

    main()
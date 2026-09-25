from bot.api.espn import get_wnba_games


def main():

    print()
    print("=" * 70)
    print("ESPN WNBA API TEST")
    print("=" * 70)

    games = get_wnba_games()

    print(
        f"Games received from ESPN: "
        f"{len(games)}"
    )

    assert isinstance(
        games,
        list
    )

    for game in games:

        print()
        print(
            f"{game['away_team']} "
            f"{game['away_score']} - "
            f"{game['home_score']} "
            f"{game['home_team']}"
        )

        print(
            f"ESPN ID: "
            f"{game['espn_game_id']}"
        )

        print(
            f"Status: "
            f"{game['status']}"
        )

    print()
    print(
        "ESPN TEST PASSED"
    )


if __name__ == "__main__":
    main()
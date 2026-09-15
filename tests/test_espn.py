from bot.api.espn import ESPNWNBAClient


def main():

    print("=" * 60)
    print("ESPN WNBA API TEST")
    print("=" * 60)

    client = ESPNWNBAClient()

    games = client.get_games()

    print()
    print(f"Games received from ESPN: {len(games)}")
    print()

    for game in games:

        print(
            f"{game['away_team']} "
            f"{game['away_score']} - "
            f"{game['home_score']} "
            f"{game['home_team']}"
        )

        print(
            f"ESPN ID: {game['espn_game_id']}"
        )

        print(
            f"Status: {game['status']}"
        )

        print("-" * 60)


if __name__ == "__main__":
    main()
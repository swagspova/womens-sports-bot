from bot.api.espn import (
    get_wnba_games,
    get_top_two_players,
)


def main():

    print("\n")
    print("=" * 70)
    print("WNBA PLAYER STATS TEST")
    print("=" * 70)

    # ========================================================
    # GET WNBA GAMES
    # ========================================================

    games = get_wnba_games()

    print(
        f"\nGames received from ESPN: "
        f"{len(games)}"
    )

    # ========================================================
    # FIND A FINAL GAME
    # ========================================================

    final_games = [
        game
        for game in games
        if game["status"] == "STATUS_FINAL"
    ]

    if not final_games:

        print(
            "\nNo final WNBA games found."
        )

        print(
            "Run this test when ESPN has "
            "completed games available."
        )

        return

    game = final_games[0]

    print(
        "\nTesting game:"
    )

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

    # ========================================================
    # GET TOP TWO
    # ========================================================

    top_players = get_top_two_players(
        game["espn_game_id"]
    )

    print(
        "\nTop Players:"
    )

    print(
        "-" * 70
    )

    for index, player in enumerate(
        top_players,
        start=1,
    ):

        print(
            f"{index}. "
            f"{player['name']}"
        )

        print(
            f"   Team: "
            f"{player['team']}"
        )

        print(
            f"   PTS: "
            f"{player['points']}"
        )

        print(
            f"   AST: "
            f"{player['assists']}"
        )

        print(
            f"   REB: "
            f"{player['rebounds']}"
        )

        print(
            f"   PRA: "
            f"{player['pra']}"
        )

        print()

    # ========================================================
    # ASSERTIONS
    # ========================================================

    assert len(top_players) <= 2

    assert len(top_players) > 0

    for player in top_players:

        assert "name" in player
        assert "team" in player
        assert "points" in player
        assert "assists" in player
        assert "rebounds" in player
        assert "pra" in player

        assert (
            player["pra"]
            ==
            player["points"]
            + player["assists"]
            + player["rebounds"]
        )

    # ========================================================
    # VERIFY SORTING
    # ========================================================

    if len(top_players) == 2:

        assert (
            top_players[0]["pra"]
            >=
            top_players[1]["pra"]
        )

    print(
        "=" * 70
    )

    print(
        "PLAYER STATS TEST PASSED"
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":
    main()
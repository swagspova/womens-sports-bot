from types import SimpleNamespace

from bot.tweet_builder import (
    build_final_score_tweet,
)


def main():

    print("\n")
    print("=" * 70)
    print("TWEET BUILDER TEST")
    print("=" * 70)

    # ========================================================
    # TEST GAME
    # ========================================================

    game = SimpleNamespace(

        id=1,

        away_team="Indiana Fever",
        home_team="New York Liberty",

        away_score=90,
        home_score=85,

        # Top player #1
        top_player_1_name="Player One",
        top_player_1_points=28,
        top_player_1_assists=7,
        top_player_1_rebounds=11,

        # Top player #2
        top_player_2_name="Player Two",
        top_player_2_points=25,
        top_player_2_assists=9,
        top_player_2_rebounds=7,
    )

    # ========================================================
    # BUILD TWEET
    # ========================================================

    tweet = build_final_score_tweet(
        game
    )

    print(
        "\nGenerated Tweet:"
    )

    print(
        "-" * 70
    )

    print(
        tweet.text
    )

    print(
        "-" * 70
    )

    print(
        f"Length: "
        f"{len(tweet.text)}/280"
    )

    # ========================================================
    # ASSERTIONS
    # ========================================================

    assert (
        "Indiana Fever 90 - 85 New York Liberty"
        in tweet.text
    )

    assert (
        "🏆 Winner: Indiana Fever"
        in tweet.text
    )

    assert (
        "Player One - 28 PTS | 7 AST | 11 REB"
        in tweet.text
    )

    assert (
        "Player Two - 25 PTS | 9 AST | 7 REB"
        in tweet.text
    )

    assert (
        "⭐ Top Performers"
        in tweet.text
    )

    assert len(tweet.text) <= 280

    assert tweet.game_id == 1

    print(
        "\n"
    )

    print(
        "=" * 70
    )

    print(
        "TWEET BUILDER TEST PASSED"
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":
    main()
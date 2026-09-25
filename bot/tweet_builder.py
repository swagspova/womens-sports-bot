from dataclasses import dataclass


MAX_TWEET_LENGTH = 280


@dataclass
class Tweet:
    text: str
    game_id: int


def build_final_score_tweet(game):
    """
    Build a WNBA final-score tweet.

    Includes:
    - Final score
    - Winning team
    - Top 2 performers
    - Points
    - Assists
    - Rebounds
    """

    # --------------------------------------------------------
    # DETERMINE WINNER
    # --------------------------------------------------------

    if game.away_score > game.home_score:
        winner = game.away_team

    elif game.home_score > game.away_score:
        winner = game.home_team

    else:
        winner = None

    # --------------------------------------------------------
    # BASE TWEET
    # --------------------------------------------------------

    lines = [
        "🏀 WNBA FINAL SCORE",
        "",
        (
            f"{game.away_team} "
            f"{game.away_score} - "
            f"{game.home_score} "
            f"{game.home_team}"
        ),
        "",
    ]

    # --------------------------------------------------------
    # WINNER
    # --------------------------------------------------------

    if winner:
        lines.append(
            f"🏆 Winner: {winner}"
        )
    else:
        lines.append(
            "🤝 Result: Tie"
        )

    # --------------------------------------------------------
    # TOP PERFORMERS
    # --------------------------------------------------------

    top_players = []

    if game.top_player_1_name:
        top_players.append(
            (
                game.top_player_1_name,
                game.top_player_1_points,
                game.top_player_1_assists,
                game.top_player_1_rebounds,
            )
        )

    if game.top_player_2_name:
        top_players.append(
            (
                game.top_player_2_name,
                game.top_player_2_points,
                game.top_player_2_assists,
                game.top_player_2_rebounds,
            )
        )

    # --------------------------------------------------------
    # ADD PLAYERS TO TWEET
    # --------------------------------------------------------

    if top_players:

        lines.extend(
            [
                "",
                "⭐ Top Performers",
            ]
        )

        for (
            name,
            points,
            assists,
            rebounds,
        ) in top_players:

            lines.append(
                (
                    f"{name} - "
                    f"{points} PTS | "
                    f"{assists} AST | "
                    f"{rebounds} REB"
                )
            )

    # --------------------------------------------------------
    # BUILD FINAL TEXT
    # --------------------------------------------------------

    text = "\n".join(lines)

    # --------------------------------------------------------
    # CHECK X/TWITTER CHARACTER LIMIT
    # --------------------------------------------------------

    if len(text) > MAX_TWEET_LENGTH:
        raise ValueError(
            f"Tweet is {len(text)} characters. "
            f"Maximum allowed is {MAX_TWEET_LENGTH}."
        )

    return Tweet(
        text=text,
        game_id=game.id,
    )
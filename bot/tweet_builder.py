from dataclasses import dataclass


MAX_TWEET_LENGTH = 280


@dataclass
class Tweet:

    text: str

    game_id: str


def build_final_score_tweet(game):

    if game.status != "STATUS_FINAL":

        raise ValueError(
            "Cannot build a final-score tweet "
            "for a non-final game."
        )

    if game.home_score > game.away_score:

        winner = game.home_team

    elif game.away_score > game.home_score:

        winner = game.away_team

    else:

        winner = None

    if winner:

        text = (

            f"🏀 WNBA FINAL SCORE\n\n"

            f"{game.away_team} "
            f"{game.away_score}\n"

            f"{game.home_team} "
            f"{game.home_score}\n\n"

            f"🏆 {winner}"

        )

    else:

        text = (

            f"🏀 WNBA FINAL SCORE\n\n"

            f"{game.away_team} "
            f"{game.away_score}\n"

            f"{game.home_team} "
            f"{game.home_score}\n\n"

            f"🤝 Tied"

        )

    if len(text) > MAX_TWEET_LENGTH:

        raise ValueError(
            "Tweet exceeds 280 characters."
        )

    return Tweet(

        text=text,

        game_id=game.espn_game_id

    )
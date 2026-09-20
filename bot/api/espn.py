import requests

from config import ESPN_WNBA_SCOREBOARD_URL


def get_wnba_games():

    response = requests.get(
        ESPN_WNBA_SCOREBOARD_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    return data.get(
        "events",
        []
    )
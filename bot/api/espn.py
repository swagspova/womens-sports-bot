from datetime import datetime

import requests


ESPN_WNBA_SCOREBOARD_URL = (
    "https://site.api.espn.com/apis/site/v2/"
    "sports/basketball/wnba/scoreboard"
)

ESPN_WNBA_SUMMARY_URL = (
    "https://site.api.espn.com/apis/site/v2/"
    "sports/basketball/wnba/summary"
)

REQUEST_TIMEOUT = 15


def _safe_int(value):
    """
    Safely convert a value to an integer.
    """
    try:
        if value is None:
            return 0

        return int(float(value))

    except (TypeError, ValueError):
        return 0


def _parse_game_date(value):
    """
    Convert ESPN's ISO-8601 date string into a Python datetime.

    Example ESPN value:
        2026-09-25T13:22:40Z

    Returns:
        datetime object
        None if the value cannot be parsed
    """

    if not value:
        return None

    try:
        # ESPN commonly returns UTC timestamps ending in Z.
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    except (TypeError, ValueError):
        return None


def get_wnba_games():
    """
    Fetch WNBA games from ESPN scoreboard API.

    Returns:
        List of dictionaries containing game information.
    """

    response = requests.get(
        ESPN_WNBA_SCOREBOARD_URL,
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    games = []

    for event in data.get("events", []):

        competitions = event.get("competitions", [])

        if not competitions:
            continue

        competition = competitions[0]

        competitors = competition.get("competitors", [])

        if len(competitors) < 2:
            continue

        away_team = None
        home_team = None

        away_score = 0
        home_score = 0

        for competitor in competitors:

            team = competitor.get("team", {})

            team_name = (
                team.get("displayName")
                or team.get("shortDisplayName")
                or team.get("name")
            )

            score = _safe_int(
                competitor.get("score")
            )

            home_away = competitor.get("homeAway")

            if home_away == "away":

                away_team = team_name
                away_score = score

            elif home_away == "home":

                home_team = team_name
                home_score = score

        status = (
            event
            .get("status", {})
            .get("type", {})
            .get("name")
        )

        # IMPORTANT:
        # ESPN returns the game date as a string.
        # SQLAlchemy DateTime requires a Python datetime.
        game_date = _parse_game_date(
            event.get("date")
        )

        games.append(
            {
                "espn_game_id": str(
                    event.get("id")
                ),
                "sport": "basketball",
                "league": "wnba",
                "game_date": game_date,
                "away_team": away_team,
                "home_team": home_team,
                "away_score": away_score,
                "home_score": home_score,
                "status": status,
            }
        )

    return games


def get_wnba_player_stats(event_id: str):
    """
    Fetch player statistics for a WNBA game.

    Statistics collected:

    - Points
    - Assists
    - Rebounds

    PRA is calculated as:

        Points + Assists + Rebounds

    Returns:
        List of player dictionaries.
    """

    response = requests.get(
        ESPN_WNBA_SUMMARY_URL,
        params={"event": event_id},
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    boxscore = data.get("boxscore", {})

    teams = boxscore.get("players", [])

    players = []

    for team_data in teams:

        team = team_data.get("team", {})

        team_name = (
            team.get("displayName")
            or team.get("shortDisplayName")
            or team.get("name")
            or ""
        )

        statistics_groups = team_data.get(
            "statistics",
            []
        )

        for group in statistics_groups:

            labels = group.get("labels", [])

            athletes = group.get(
                "athletes",
                []
            )

            if not labels:
                continue

            for athlete_data in athletes:

                athlete = athlete_data.get(
                    "athlete",
                    {}
                )

                name = (
                    athlete.get("displayName")
                    or athlete.get("fullName")
                    or athlete.get("shortName")
                )

                stats = athlete_data.get(
                    "stats",
                    []
                )

                if not name or not stats:
                    continue

                stat_map = dict(
                    zip(labels, stats)
                )

                points = _safe_int(
                    stat_map.get("PTS")
                )

                assists = _safe_int(
                    stat_map.get("AST")
                )

                rebounds = _safe_int(
                    stat_map.get("REB")
                )

                pra = (
                    points
                    + assists
                    + rebounds
                )

                players.append(
                    {
                        "name": name,
                        "team": team_name,
                        "points": points,
                        "assists": assists,
                        "rebounds": rebounds,
                        "pra": pra,
                    }
                )

    return players


def get_top_two_players(event_id: str):
    """
    Get the top two players from both teams.

    Ranking criteria:

    1. PRA = Points + Assists + Rebounds
    2. Points
    3. Assists
    4. Rebounds
    5. Player name

    Returns:
        Maximum of two players.
    """

    players = get_wnba_player_stats(
        event_id
    )

    players.sort(
        key=lambda player: (
            player["pra"],
            player["points"],
            player["assists"],
            player["rebounds"],
            player["name"],
        ),
        reverse=True,
    )

    return players[:2]
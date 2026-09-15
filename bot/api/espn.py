import requests
from datetime import datetime


ESPN_URL = (
    "https://site.api.espn.com/apis/site/v2/"
    "sports/basketball/wnba/scoreboard"
)


class ESPNWNBAClient:

    def __init__(self):
        self.url = ESPN_URL

    def get_scoreboard(self, date=None):
        """
        Retrieve WNBA scoreboard data from ESPN.

        date:
            YYYYMMDD
        """

        params = {}

        if date:
            params["dates"] = date

        response = requests.get(
            self.url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json()

    def get_games(self, date=None):
        """
        Retrieve and normalize WNBA games.
        """

        data = self.get_scoreboard(date)

        games = []

        for event in data.get("events", []):

            competitions = event.get("competitions", [])

            if not competitions:
                continue

            competition = competitions[0]

            competitors = competition.get(
                "competitors",
                []
            )

            home_team = None
            away_team = None

            home_score = None
            away_score = None

            for competitor in competitors:

                team = competitor.get("team", {})

                team_name = (
                    team.get("displayName")
                    or team.get("shortDisplayName")
                    or team.get("name")
                )

                score = competitor.get("score")

                try:
                    score = int(score)
                except (TypeError, ValueError):
                    score = None

                if competitor.get("homeAway") == "home":
                    home_team = team_name
                    home_score = score

                elif competitor.get("homeAway") == "away":
                    away_team = team_name
                    away_score = score

            status = (
                competition
                .get("status", {})
                .get("type", {})
                .get("name")
            )

            game_date = event.get("date")

            if game_date:
                game_date = datetime.fromisoformat(
                    game_date.replace("Z", "+00:00")
                )

            games.append(
                {
                    "espn_game_id": event.get("id"),
                    "game_date": game_date,
                    "away_team": away_team,
                    "home_team": home_team,
                    "away_score": away_score,
                    "home_score": home_score,
                    "status": status,
                }
            )

        return games
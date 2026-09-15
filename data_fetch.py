import requests


ESPN_URL = (
    "https://site.api.espn.com/apis/site/v2/sports/"
    "basketball/wnba/scoreboard"
)


def fetch_wnba_scoreboard():

    try:

        response = requests.get(
            ESPN_URL,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        print("ESPN request timed out.")

        return {}

    except requests.exceptions.RequestException as error:

        print(
            f"ESPN request failed: {error}"
        )

        return {}

    except ValueError:

        print(
            "ESPN returned invalid JSON."
        )

        return {}


def get_events():

    data = fetch_wnba_scoreboard()

    return data.get("events", [])
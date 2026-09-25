import os
from dotenv import load_dotenv

load_dotenv()


BOT_NAME = os.getenv(
    "BOT_NAME",
    "womens-sports-bot"
)

SPORT = os.getenv(
    "SPORT",
    "wnba"
)


ESPN_WNBA_SCOREBOARD_URL = os.getenv(
    "ESPN_WNBA_SCOREBOARD_URL",
    "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard"
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./womens_sports.db"
)


POLL_INTERVAL_SECONDS = int(
    os.getenv(
        "POLL_INTERVAL_SECONDS",
        "120"
    )
)


TWITTER_ENABLED = (
    os.getenv(
        "TWITTER_ENABLED",
        "false"
    ).lower()
    == "true"
)


TWITTER_API_KEY = os.getenv(
    "TWITTER_API_KEY",
    ""
)

TWITTER_API_SECRET = os.getenv(
    "TWITTER_API_SECRET",
    ""
)

TWITTER_ACCESS_TOKEN = os.getenv(
    "TWITTER_ACCESS_TOKEN",
    ""
)

TWITTER_ACCESS_TOKEN_SECRET = os.getenv(
    "TWITTER_ACCESS_TOKEN_SECRET",
    ""
)
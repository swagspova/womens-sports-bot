import os

from dotenv import load_dotenv


load_dotenv()


# ---------------------------------------------------------
# Application
# ---------------------------------------------------------

APP_NAME = os.getenv(
    "APP_NAME",
    "womens-sports-bot"
)

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development"
)

SPORT = os.getenv(
    "SPORT",
    "wnba"
)


# ---------------------------------------------------------
# ESPN
# ---------------------------------------------------------

ESPN_WNBA_SCOREBOARD_URL = os.getenv(
    "ESPN_WNBA_SCOREBOARD_URL",
    "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard"
)


# ---------------------------------------------------------
# Twitter / X
# ---------------------------------------------------------

TWITTER_API_KEY = os.getenv(
    "TWITTER_API_KEY"
)

TWITTER_API_SECRET = os.getenv(
    "TWITTER_API_SECRET"
)

TWITTER_ACCESS_TOKEN = os.getenv(
    "TWITTER_ACCESS_TOKEN"
)

TWITTER_ACCESS_TOKEN_SECRET = os.getenv(
    "TWITTER_ACCESS_TOKEN_SECRET"
)


TWITTER_DRY_RUN = os.getenv(
    "TWITTER_DRY_RUN",
    "true"
).lower() == "true"
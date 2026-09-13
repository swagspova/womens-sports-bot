import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv("APP_NAME", "womens-sports-bot")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
SPORT = os.getenv("SPORT", "wnba")


def show_config():
    print("=" * 60)
    print("WOMEN'S SPORTS BOT CONFIGURATION")
    print("=" * 60)

    print(f"App Name   : {APP_NAME}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Sport      : {SPORT}")

    print("=" * 60)
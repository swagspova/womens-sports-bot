import sys
from pathlib import Path

# Add the project root to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from config import APP_NAME, ENVIRONMENT, SPORT


def test_app_name():
    assert APP_NAME == "womens-sports-bot"


def test_environment():
    assert ENVIRONMENT == "development"


def test_sport():
    assert SPORT == "wnba"
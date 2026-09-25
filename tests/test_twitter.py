import os

os.environ["TWITTER_ENABLED"] = "false"

from bot.twitter_client import TwitterClient


def main():

    print()
    print("=" * 70)
    print("TWITTER DRY RUN TEST")
    print("=" * 70)

    client = TwitterClient()

    result = client.send_tweet(
        "🏀 WNBA FINAL\n\n"
        "Indiana Fever 90 - 85 New York Liberty"
    )

    print(
        result
    )

    assert result["success"] is True

    assert result["dry_run"] is True

    assert result["tweet_id"] is None

    print()
    print(
        "TWITTER DRY RUN TEST PASSED"
    )


if __name__ == "__main__":
    main()
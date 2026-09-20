import os

from dotenv import load_dotenv


load_dotenv()


class TwitterClient:
    """
    Handles publishing tweets to X/Twitter.

    During Day 5 development, DRY RUN mode is used
    so no real tweet is published.
    """

    def __init__(self):

        self.dry_run = (
            os.getenv(
                "TWITTER_DRY_RUN",
                "true"
            ).lower()
            == "true"
        )

        self.client = None

        if not self.dry_run:

            import tweepy

            api_key = os.getenv(
                "TWITTER_API_KEY"
            )

            api_secret = os.getenv(
                "TWITTER_API_SECRET"
            )

            access_token = os.getenv(
                "TWITTER_ACCESS_TOKEN"
            )

            access_token_secret = os.getenv(
                "TWITTER_ACCESS_TOKEN_SECRET"
            )

            if not all([
                api_key,
                api_secret,
                access_token,
                access_token_secret
            ]):

                raise ValueError(
                    "Twitter credentials are missing."
                )

            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )

    def post_tweet(self, text):

        if not text:

            raise ValueError(
                "Tweet text cannot be empty."
            )

        if len(text) > 280:

            raise ValueError(
                "Tweet exceeds 280 characters."
            )

        if self.dry_run:

            print()
            print("=" * 60)
            print("TWITTER DRY RUN")
            print("=" * 60)

            print("\nTweet that would be posted:\n")

            print(text)

            print("\n" + "=" * 60)

            return {
                "success": True,
                "tweet_id": None,
                "dry_run": True
            }

        response = self.client.create_tweet(
            text=text
        )

        tweet_id = response.data["id"]

        return {
            "success": True,
            "tweet_id": str(tweet_id),
            "dry_run": False
        }
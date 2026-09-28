import os

import requests
from requests_oauthlib import OAuth1


class TwitterClient:
    API_URL = "https://api.x.com/2/tweets"

    def __init__(self):

        self.enabled = (
            os.getenv(
                "TWITTER_ENABLED",
                "false"
            ).lower()
            == "true"
        )

        self.api_key = os.getenv(
            "TWITTER_API_KEY"
        )

        self.api_secret = os.getenv(
            "TWITTER_API_SECRET"
        )

        self.access_token = os.getenv(
            "TWITTER_ACCESS_TOKEN"
        )

        self.access_token_secret = os.getenv(
            "TWITTER_ACCESS_TOKEN_SECRET"
        )

    def post_tweet(self, text):
        """
        Publish a text post to X using
        OAuth 1.0a User Context.

        Returns
        -------
        dict
            Result of the X API request.
        """

        # ========================================================
        # DRY RUN
        # ========================================================

        if not self.enabled:

            print("\nDRY RUN - Tweet:")
            print(text)

            return {
                "success": True,
                "dry_run": True,
                "tweet_id": None
            }

        # ========================================================
        # VALIDATE CREDENTIALS
        # ========================================================

        credentials = {
            "TWITTER_API_KEY": self.api_key,
            "TWITTER_API_SECRET": self.api_secret,
            "TWITTER_ACCESS_TOKEN": self.access_token,
            "TWITTER_ACCESS_TOKEN_SECRET":
                self.access_token_secret,
        }

        missing = [
            name
            for name, value in credentials.items()
            if not value
        ]

        if missing:

            raise RuntimeError(
                "Missing X OAuth 1.0a credentials: "
                + ", ".join(missing)
            )

        # ========================================================
        # OAUTH 1.0a USER CONTEXT
        # ========================================================

        auth = OAuth1(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret,
        )

        # ========================================================
        # POST TWEET
        # ========================================================

        response = requests.post(
            self.API_URL,
            auth=auth,
            json={
                "text": text
            },
            timeout=30
        )

        # ========================================================
        # HANDLE ERROR
        # ========================================================

        if not response.ok:

            raise RuntimeError(
                f"X API error "
                f"{response.status_code}: "
                f"{response.text}"
            )

        # ========================================================
        # PARSE RESPONSE
        # ========================================================

        data = response.json()

        tweet_id = data["data"]["id"]

        print(
            f"\nTweet posted successfully: "
            f"{tweet_id}"
        )

        return {
            "success": True,
            "dry_run": False,
            "tweet_id": tweet_id
        }
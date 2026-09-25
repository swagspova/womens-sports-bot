import os
import requests


class TwitterClient:

    API_URL = "https://api.x.com/2/tweets"

    def __init__(self):
        self.enabled = os.getenv(
            "TWITTER_ENABLED",
            "false"
        ).lower() == "true"

        self.access_token = os.getenv(
            "X_USER_ACCESS_TOKEN"
        )

    def post_tweet(self, text):
        """
        Publish a text post to X.

        Returns:
            dict containing the API response
        """

        if not self.enabled:
            print("\nDRY RUN - Tweet:")
            print(text)
            return {
                "success": True,
                "dry_run": True,
                "tweet_id": None
            }

        if not self.access_token:
            raise RuntimeError(
                "X_USER_ACCESS_TOKEN is not configured"
            )

        response = requests.post(
            self.API_URL,
            headers={
                "Authorization": (
                    f"Bearer {self.access_token}"
                ),
                "Content-Type": "application/json"
            },
            json={
                "text": text
            },
            timeout=30
        )

        if not response.ok:
            raise RuntimeError(
                f"X API error "
                f"{response.status_code}: "
                f"{response.text}"
            )

        data = response.json()

        tweet_id = data["data"]["id"]

        print(
            f"Tweet posted successfully: {tweet_id}"
        )

        return {
            "success": True,
            "dry_run": False,
            "tweet_id": tweet_id
        }
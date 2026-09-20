class DryRunTwitterClient:

    def post_tweet(self, tweet_text):

        print("\n" + "=" * 60)
        print("DRY RUN — TWEET NOT PUBLISHED")
        print("=" * 60)

        print(tweet_text)

        print("=" * 60)

        return {
            "dry_run": True,
            "tweet_id": "DRY_RUN"
        }
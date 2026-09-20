from bot.twitter_client import TwitterClient


def main():

    print("\n")
    print("=" * 60)
    print("TWITTER CLIENT TEST")
    print("=" * 60)

    client = TwitterClient()

    print(
        f"\nDry run: "
        f"{client.dry_run}"
    )

    result = client.post_tweet(
        "🏀 WNBA FINAL\n\n"
        "Indiana Fever 103\n"
        "Toronto Tempo 85\n\n"
        "🏆 Indiana Fever"
    )

    print("\nResult:")
    print(result)

    print("\n")
    print("=" * 60)
    print("TWITTER CLIENT TEST PASSED")
    print("=" * 60)


if __name__ == "__main__":

    main()
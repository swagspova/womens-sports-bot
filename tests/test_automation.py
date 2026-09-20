from bot.services.game_processor import GameProcessor


def main():

    print()
    print("=" * 70)
    print("DAY 6 AUTOMATION TEST")
    print("=" * 70)

    processor = GameProcessor(
        dry_run=True
    )

    result = processor.process_completed_games()

    print()
    print("=" * 70)
    print("AUTOMATION TEST COMPLETE")
    print("=" * 70)

    print(
        f"Games processed: {result}"
    )


if __name__ == "__main__":
    main()
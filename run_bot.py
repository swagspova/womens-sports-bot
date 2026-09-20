from bot.services.scheduler import Scheduler


def main():

    print()
    print("=" * 70)
    print("WOMEN'S SPORTS BOT")
    print("DAY 6 AUTOMATION TEST")
    print("=" * 70)

    scheduler = Scheduler(
        interval=120,
        dry_run=True
    )

    print()
    print("Running one scheduler cycle...")
    print()

    scheduler.run()

    print()
    print("=" * 70)
    print("SCHEDULER TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
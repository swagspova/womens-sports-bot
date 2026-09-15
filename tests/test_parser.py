from data_fetch import get_events
from espn_parser import parse_event, validate_game


print("=" * 60)
print("ESPN PARSER + VALIDATION TEST")
print("=" * 60)


# ----------------------------------------------------------
# 1. Get ESPN events
# ----------------------------------------------------------

events = get_events()

print()
print(
    "Events received:",
    len(events)
)
print()


# ----------------------------------------------------------
# 2. Parse each event
# ----------------------------------------------------------

valid_games = 0
invalid_games = 0


for event in events:

    print("-" * 60)

    game = parse_event(event)


    # ------------------------------------------------------
    # Check parsing
    # ------------------------------------------------------

    if game is None:

        print("Parser returned None.")

        invalid_games += 1

        continue


    # ------------------------------------------------------
    # Display parsed game
    # ------------------------------------------------------

    print("Parsed Game:")

    print(
        f"ESPN Game ID : "
        f"{game['espn_game_id']}"
    )

    print(
        f"Date         : "
        f"{game['date']}"
    )

    print(
        f"Away Team    : "
        f"{game['away_team']}"
    )

    print(
        f"Away Score   : "
        f"{game['away_score']}"
    )

    print(
        f"Home Team    : "
        f"{game['home_team']}"
    )

    print(
        f"Home Score   : "
        f"{game['home_score']}"
    )

    print(
        f"Status       : "
        f"{game['status']}"
    )


    # ------------------------------------------------------
    # Validate game
    # ------------------------------------------------------

    print()

    if validate_game(game):

        print("VALIDATION: PASS")

        valid_games += 1

    else:

        print("VALIDATION: FAIL")

        invalid_games += 1


# ----------------------------------------------------------
# 3. Summary
# ----------------------------------------------------------

print()
print("=" * 60)
print("VALIDATION SUMMARY")
print("=" * 60)

print(
    f"Total events : {len(events)}"
)

print(
    f"Valid games  : {valid_games}"
)

print(
    f"Invalid games: {invalid_games}"
)

print()


# ----------------------------------------------------------
# 4. Final result
# ----------------------------------------------------------

if invalid_games == 0:

    print(
        "All ESPN games passed validation."
    )

else:

    print(
        "Some ESPN games failed validation."
    )


print()
print("=" * 60)
print("ESPN PARSER + VALIDATION TEST COMPLETE")
print("=" * 60)
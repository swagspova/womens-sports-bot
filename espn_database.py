from database import init_db, get_session, Game
from data_fetch import get_events
from espn_parser import parse_event


def save_game(game_data):
    """
    Insert a new game or update an existing game.
    """

    session = get_session()

    try:

        existing_game = (
            session.query(Game)
            .filter(
                Game.espn_game_id
                == game_data["espn_game_id"]
            )
            .first()
        )

        if existing_game:

            existing_game.sport = game_data["sport"]
            existing_game.league = game_data["league"]
            existing_game.date = game_data["date"]
            existing_game.home_team = game_data["home_team"]
            existing_game.away_team = game_data["away_team"]
            existing_game.home_score = game_data["home_score"]
            existing_game.away_score = game_data["away_score"]
            existing_game.status = game_data["status"]

            print(
                f"Updated game: "
                f"{game_data['away_team']} "
                f"@ "
                f"{game_data['home_team']}"
            )

        else:

            new_game = Game(
                espn_game_id=game_data["espn_game_id"],
                sport=game_data["sport"],
                league=game_data["league"],
                date=game_data["date"],
                home_team=game_data["home_team"],
                away_team=game_data["away_team"],
                home_score=game_data["home_score"],
                away_score=game_data["away_score"],
                status=game_data["status"],
            )

            session.add(new_game)

            print(
                f"Inserted game: "
                f"{game_data['away_team']} "
                f"@ "
                f"{game_data['home_team']}"
            )

        session.commit()

    except Exception:

        session.rollback()
        raise

    finally:

        session.close()


def sync_espn_games():
    """
    Fetch games from ESPN and save them to SQLite.
    """

    events = get_events()

    print(
        f"Games received from ESPN: {len(events)}"
    )

    saved_games = 0

    for event in events:

        game_data = parse_event(event)

        if game_data is None:
            print("Skipping invalid ESPN event.")
            continue

        save_game(game_data)

        saved_games += 1

    return saved_games


if __name__ == "__main__":

    print("=" * 60)
    print("ESPN → DATABASE SYNC")
    print("=" * 60)

    init_db()

    count = sync_espn_games()

    print()
    print(
        f"Games processed: {count}"
    )
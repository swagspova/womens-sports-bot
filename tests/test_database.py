import uuid
from datetime import datetime, timezone

from database import (
    init_db,
    get_session,
    save_game,
    game_exists,
    get_game,
    get_unposted_games,
    mark_game_posted,
)


def main():

    print("\n")
    print("=" * 60)
    print("DATABASE TEST")
    print("=" * 60)

    # ========================================================
    # INITIALIZE DATABASE
    # ========================================================

    init_db()

    db = get_session()

    try:

        # ====================================================
        # UNIQUE TEST GAME
        # ====================================================

        test_espn_id = (
            f"TEST_{uuid.uuid4().hex}"
        )

        game_data = {
            "espn_game_id": test_espn_id,
            "sport": "basketball",
            "league": "wnba",
            "game_date": datetime.now(
                timezone.utc
            ),
            "away_team": "Test Away Team",
            "home_team": "Test Home Team",
            "away_score": 90,
            "home_score": 85,
            "status": "STATUS_FINAL",
        }

        # ====================================================
        # SAVE GAME
        # ====================================================

        game = save_game(
            db,
            game_data,
        )

        print(
            f"Created game ID: {game.id}"
        )

        assert game.id is not None

        # ====================================================
        # GAME EXISTS
        # ====================================================

        assert game_exists(
            db,
            test_espn_id,
        )

        print(
            "game_exists(): PASS"
        )

        # ====================================================
        # GET GAME
        # ====================================================

        fetched_game = get_game(
            db,
            test_espn_id,
        )

        assert fetched_game is not None

        assert (
            fetched_game.espn_game_id
            == test_espn_id
        )

        print(
            "get_game(): PASS"
        )

        # ====================================================
        # GET UNPOSTED GAMES
        # ====================================================

        games = get_unposted_games(
            db
        )

        assert any(
            g.id == game.id
            for g in games
        )

        print(
            "get_unposted_games(): PASS"
        )

        # ====================================================
        # MARK POSTED
        # ====================================================

        mark_game_posted(
            db,
            game.id,
        )

        updated_game = get_game(
            db,
            test_espn_id,
        )

        assert updated_game.posted is True

        print(
            "mark_game_posted(): PASS"
        )

        # ====================================================
        # VERIFY REMOVED FROM UNPOSTED
        # ====================================================

        games_after_post = (
            get_unposted_games(db)
        )

        assert not any(
            g.id == game.id
            for g in games_after_post
        )

        print(
            "posted game removed from "
            "unposted list: PASS"
        )

        # ====================================================
        # COMPLETE
        # ====================================================

        print("\n")
        print("=" * 60)
        print("DATABASE TEST PASSED")
        print("=" * 60)

    finally:

        db.close()


if __name__ == "__main__":
    main()
from datetime import datetime


def parse_event(event):
    """
    Convert one ESPN event into our internal game format.
    """

    # ----------------------------------------------------------
    # 1. Get ESPN Game ID
    # ----------------------------------------------------------

    espn_game_id = event.get("id")

    if not espn_game_id:
        return None


    # ----------------------------------------------------------
    # 2. Get Competition
    # ----------------------------------------------------------

    competitions = event.get("competitions", [])

    if not competitions:
        return None

    competition = competitions[0]


    # ----------------------------------------------------------
    # 3. Get Competitors
    # ----------------------------------------------------------

    competitors = competition.get("competitors", [])

    if len(competitors) < 2:
        return None


    # ----------------------------------------------------------
    # 4. Initialize Team Information
    # ----------------------------------------------------------

    home_team = None
    away_team = None

    home_score = None
    away_score = None


    # ----------------------------------------------------------
    # 5. Extract Home and Away Teams
    # ----------------------------------------------------------

    for competitor in competitors:

        team = competitor.get("team", {})

        team_name = (
            team.get("displayName")
            or team.get("name")
            or team.get("abbreviation")
        )

        score = competitor.get("score")

        # Convert score to integer
        try:

            score = int(score) if score is not None else None

        except (TypeError, ValueError):

            score = None


        # Determine whether team is home or away

        if competitor.get("homeAway") == "home":

            home_team = team_name
            home_score = score

        elif competitor.get("homeAway") == "away":

            away_team = team_name
            away_score = score


    # ----------------------------------------------------------
    # 6. Get Game Status
    # ----------------------------------------------------------

    status = (
        event
        .get("status", {})
        .get("type", {})
        .get("name")
    )


    # ----------------------------------------------------------
    # 7. Get Game Date
    # ----------------------------------------------------------

    date_value = event.get("date")

    game_date = None

    if date_value:

        try:

            game_date = datetime.fromisoformat(
                date_value.replace("Z", "+00:00")
            )

        except ValueError:

            game_date = None


    # ----------------------------------------------------------
    # 8. Create Normalized Game
    # ----------------------------------------------------------

    return {
        "espn_game_id": espn_game_id,
        "sport": "basketball",
        "league": "WNBA",
        "date": game_date,
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "status": status,
    }


def validate_game(game):
    """
    Validate normalized game data.

    Returns:
        True  -> game is valid
        False -> game is invalid
    """

    # ----------------------------------------------------------
    # 1. Check that game exists
    # ----------------------------------------------------------

    if not game:

        return False


    # ----------------------------------------------------------
    # 2. Required fields
    # ----------------------------------------------------------

    required_fields = [
        "espn_game_id",
        "sport",
        "league",
        "home_team",
        "away_team",
        "status",
    ]


    # ----------------------------------------------------------
    # 3. Check required fields
    # ----------------------------------------------------------

    for field in required_fields:

        value = game.get(field)

        if value is None or value == "":

            print(
                f"Validation failed: missing {field}"
            )

            return False


    # ----------------------------------------------------------
    # 4. Check that home and away teams are different
    # ----------------------------------------------------------

    if game["home_team"] == game["away_team"]:

        print(
            "Validation failed: "
            "home team and away team are the same"
        )

        return False


    # ----------------------------------------------------------
    # 5. Check ESPN Game ID
    # ----------------------------------------------------------

    if not str(game["espn_game_id"]).strip():

        print(
            "Validation failed: invalid ESPN Game ID"
        )

        return False


    # ----------------------------------------------------------
    # 6. Check sport
    # ----------------------------------------------------------

    if game["sport"] != "basketball":

        print(
            "Validation failed: "
            "sport is not basketball"
        )

        return False


    # ----------------------------------------------------------
    # 7. Check league
    # ----------------------------------------------------------

    if game["league"] != "WNBA":

        print(
            "Validation failed: "
            "league is not WNBA"
        )

        return False


    # ----------------------------------------------------------
    # 8. Validate scores when available
    # ----------------------------------------------------------

    if game["home_score"] is not None:

        if not isinstance(game["home_score"], int):

            print(
                "Validation failed: "
                "home score is not an integer"
            )

            return False


        if game["home_score"] < 0:

            print(
                "Validation failed: "
                "home score cannot be negative"
            )

            return False


    if game["away_score"] is not None:

        if not isinstance(game["away_score"], int):

            print(
                "Validation failed: "
                "away score is not an integer"
            )

            return False


        if game["away_score"] < 0:

            print(
                "Validation failed: "
                "away score cannot be negative"
            )

            return False


    # ----------------------------------------------------------
    # 9. Validate final games
    # ----------------------------------------------------------

    if game["status"] == "STATUS_FINAL":

        if game["home_score"] is None:

            print(
                "Validation failed: "
                "final game has no home score"
            )

            return False


        if game["away_score"] is None:

            print(
                "Validation failed: "
                "final game has no away score"
            )

            return False


    # ----------------------------------------------------------
    # 10. Everything passed
    # ----------------------------------------------------------

    return True
from database import get_session
from models import BotLog


def log_message(level, message):
    """
    Save a bot log message to the database.
    """

    session = get_session()

    try:

        log = BotLog(
            level=level,
            message=message
        )

        session.add(log)
        session.commit()

        print(f"[{level}] {message}")

    finally:

        session.close()


def log_info(message):
    """
    Save an informational message.
    """

    log_message(
        "INFO",
        message
    )


def log_warning(message):
    """
    Save a warning message.
    """

    log_message(
        "WARNING",
        message
    )


def log_error(message):
    """
    Save an error message.
    """

    log_message(
        "ERROR",
        message
    )
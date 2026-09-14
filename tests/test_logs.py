from database import init_db, get_session
from logger import (
    log_info,
    log_warning,
    log_error
)


def main():

    print("\n")
    print("=" * 60)
    print("LOGGER TEST")
    print("=" * 60)

    init_db()

    print("\nWriting test logs...\n")

    log_info(
        "WNBA bot started"
    )

    log_warning(
        "This is a test warning"
    )

    log_error(
        "This is a test error"
    )

    print("\nLogs saved successfully.")

    print("\n")
    print("=" * 60)
    print("LOGGER TEST COMPLETE")
    print("=" * 60)
    print("\n")


if __name__ == "__main__":
    main()
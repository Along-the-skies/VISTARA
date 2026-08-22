import subprocess
import sys
from pathlib import Path

from config import DATABASE_PATH


BASE_DIR = Path(__file__).resolve().parent
APP_FILE = BASE_DIR / "frontend" / "app.py"
SETUP_FILE = BASE_DIR / "setup_data.py"


def is_setup_complete():
    database_path = Path(DATABASE_PATH)

    if not database_path.exists():
        return False

    return True


def main():
    if not is_setup_complete():
        print("VISTARA dataset is not set up yet.")
        print("Running setup...\n")

        if getattr(sys, "frozen", False):
            import setup_data

            setup_data.main()
        else:
            subprocess.run(
                [sys.executable, str(SETUP_FILE)],
                check=True,
                cwd=BASE_DIR
            )

    print("Starting VISTARA...")

    if getattr(sys, "frozen", False):
        from frontend import app

        return

    subprocess.run(
        [sys.executable, str(APP_FILE)],
        check=True,
        cwd=BASE_DIR
    )


if __name__ == "__main__":
    main()
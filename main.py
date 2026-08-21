import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
APP_FILE = BASE_DIR / "frontend" / "app.py"

def main():
    subprocess.run(
        [sys.executable,str(APP_FILE)],
        check=True
    )

if __name__ == "__main__":
    main()
from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent

DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "VISTARA"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATA_DIR / "local_google.db"
FILE_PATHS_FILE = DATA_DIR / "file_paths.json"
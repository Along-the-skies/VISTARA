from pathlib import Path

ROOT_DIR = Path(__file__).parent
DATA_DIR = ROOT_DIR/"data"
DATABASE_PATH = DATA_DIR/"local_google.db"
FILE_PATHS_FILE = DATA_DIR/"file_paths.json"
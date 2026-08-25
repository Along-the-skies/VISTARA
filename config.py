from pathlib import Path
import os
import sys


if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys._MEIPASS)
else:
    ROOT_DIR = Path(__file__).resolve().parent


DATA_DIR = Path(
    os.environ.get("LOCALAPPDATA", Path.home())
) / "VISTARA"

DATA_DIR.mkdir(parents=True, exist_ok=True)


DATABASE_PATH = DATA_DIR / "local_google.db"
FILE_PATHS_FILE = DATA_DIR / "file_paths.json"


MODEL_DIR = ROOT_DIR / "models" / "all_MiniLM_L6_v2"

MODEL_PATH = MODEL_DIR / "model.onnx"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"
TOKENIZER_CONFIG_PATH = MODEL_DIR / "tokenizer_config.json"
VOCAB_PATH = MODEL_DIR / "vocab.txt"
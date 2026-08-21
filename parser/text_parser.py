from pathlib import Path


def extract_text(path:Path) -> str:
    try:
        return path.read_text(encoding="utf-8",errors="ignore")
    except (OSError,UnicodeError):
        return ""

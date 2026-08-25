import subprocess
import sys
from pathlib import Path

from config import DATABASE_PATH


BASE_DIR = Path(__file__).resolve().parent
APP_FILE = BASE_DIR / "frontend" / "app.py"
SETUP_FILE = BASE_DIR / "setup_data.py"


REQUIRED_TABLES = {
    "documents",
    "documents_fts",
    "chunks",
    "chunks_fts",
    "chunk_embeddings",
}


def is_setup_complete():
    database_path = Path(DATABASE_PATH)

    if not database_path.exists():
        return False

    try:
        import sqlite3

        connection = sqlite3.connect(database_path)

        # Check required tables
        rows = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type IN ('table', 'virtual table')
        """).fetchall()

        tables = {row[0] for row in rows}

        if not REQUIRED_TABLES.issubset(tables):
            connection.close()
            return False

        # Check required columns
        columns = {
            row[1]
            for row in connection.execute(
                "PRAGMA table_info(documents)"
            ).fetchall()
        }

        required_columns = {
            "id",
            "path",
            "title",
            "content",
            "file_type",
            "file_size",
            "created_at",
            "modified_at",
            "indexed_at",
            "content_hash",
            "is_sensitive",
        }

        if not required_columns.issubset(columns):
            connection.close()
            return False

        # Make sure dataset actually contains documents
        document_count = connection.execute(
            "SELECT COUNT(*) FROM documents"
        ).fetchone()[0]

        if document_count == 0:
            connection.close()
            return False

        connection.close()

        return True

    except Exception as error:
        print(f"Database validation failed: {error}")
        return False


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
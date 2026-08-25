from library.scanner import get_file_paths
from indexer.ingest import ingest_files
from database.db import (
    init_db,
    rebuild_fts,
    add_sensitive_column,
    mark_sensitive_documents,
)


def main():
    print("VISTARA dataset setup")
    print("=" * 30)

    print("\nInitializing database...")
    init_db()

    print("\nChecking database schema...")
    add_sensitive_column()

    print("\nScanning for files...")
    paths = get_file_paths()

    print(f"\nFound {len(paths)} supported files.")

    if not paths:
        print("No supported files found.")
        return

    print("\nIngesting files...")
    ingest_files(paths)

    print("\nRebuilding search indexes...")
    rebuild_fts()

    print("\nChecking sensitive files...")
    mark_sensitive_documents()

    print("\nDataset setup complete! 🚀")


if __name__ == "__main__":
    main()
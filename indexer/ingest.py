from pathlib import Path
import hashlib
from datetime import datetime

from database.db import get_connection
from parser.text_parser import extract_text as extract_text_file
from parser.pdf_parser import extract_text as extract_text_pdf
from parser.docx_parser import extract_text as extract_text_docx
from  indexer.chunker import chunk_text

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
}


def calculate_hash(content:str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def extract_content(path:Path) -> str:
    extension = path.suffix.lower()

    if extension in {".txt",".md"}:
        return extract_text_file(path)
    
    if extension == ".pdf":
        return extract_text_pdf(path)

    if extension == ".docx":
            return extract_text_docx(path)

    return ""


def ingest_file(path:Path) -> dict | None:
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
          return None

    try:
          content = extract_content(path)

          stat = path.stat()

          return {
               "path":str(path),
               "title":path.stem,
               "content":content,
               "file_type":path.suffix.lower(),
               "file_size":stat.st_size,
               "created_at":stat.st_ctime,
               "modified_at":stat.st_mtime,
               "content_hash":calculate_hash(content),
          }
    except (OSError , ValueError):
         return None


def save_document(document: dict) -> str:
    connection = get_connection()

    existing = connection.execute(
        """
        SELECT id, content_hash
        FROM documents
        WHERE path = ?
        """,
        (document["path"],)
    ).fetchone()

    if existing:
        document_id, old_hash = existing

        if old_hash == document["content_hash"]:
            connection.close()
            return "unchanged"

        connection.execute("""
            DELETE FROM chunks
            WHERE document_id = ?
        """, (document_id,))

        connection.execute(
            """
            UPDATE documents
            SET
                title = ?,
                content = ?,
                file_type = ?,
                file_size = ?,
                created_at = ?,
                modified_at = ?,
                indexed_at = ?,
                content_hash = ?
            WHERE id = ?
            """,
            (
                document["title"],
                document["content"],
                document["file_type"],
                document["file_size"],
                document["created_at"],
                document["modified_at"],
                datetime.now().isoformat(),
                document["content_hash"],
                document_id,
            )
        )

        chunks = chunk_text(document["content"])

        for chunk in chunks:
            connection.execute(
                """
                INSERT INTO chunks (document_id, content)
                VALUES (?, ?)
                """,
                (document_id, chunk)
            )

        connection.commit()
        connection.close()

        return "updated"

    connection.execute(
        """
        INSERT INTO documents (
            path,
            title,
            content,
            file_type,
            file_size,
            created_at,
            modified_at,
            indexed_at,
            content_hash
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            document["path"],
            document["title"],
            document["content"],
            document["file_type"],
            document["file_size"],
            document["created_at"],
            document["modified_at"],
            datetime.now().isoformat(),
            document["content_hash"],
        )
    )

    document_id = connection.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    chunks = chunk_text(document["content"])

    for chunk in chunks:
        connection.execute(
            """
            INSERT INTO chunks (document_id, content)
            VALUES (?, ?)
            """,
            (document_id, chunk)
        )

    connection.commit()
    connection.close()

    return "inserted"



def ingest_files(paths:list[str]) -> None:
    total = len(paths)

    inserted = 0
    updated = 0 
    unchanged = 0
    failed = 0 

    for index,path_string in enumerate(paths,start=1):
        path=Path(path_string)

        print(f"[{index}/{total}] {path}")

        document = ingest_file(path)

        if document is None:
            failed += 1
            continue

        result = save_document(document)

        if result == "inserted":
             inserted += 1
        elif result == "updated":
            updated += 1
        elif result == "unchanged":
             unchanged += 1


    print("\nIngestion complete!")
    print(f"Inserted:   {inserted}")
    print(f"Updated:    {updated}")
    print(f"Unchanged:  {unchanged}")
    print(f"Failed:     {failed}")

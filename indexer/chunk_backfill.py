from database.db import get_connection
from indexer.chunker import chunk_text

def backfill_chunks():
    connection = get_connection()

    documents = connection.execute("""
        SELECT id, content
        FROM documents
        WHERE id NOT IN (
            SELECT document_id
            FROM chunks
        )
    """).fetchall()

    for document_id, content in documents:
        chunks = chunk_text(content)

        for chunk in chunks:
            connection.execute("""
                INSERT INTO chunks (document_id, content)
                VALUES (?, ?)
            """, (document_id, chunk))
        print(f"{document_id} done")

    connection.commit()
    connection.close()

    print(f"Backfilled chunks for {len(documents)} documents.")
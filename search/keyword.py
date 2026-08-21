from database.db import get_connection





def keyword_search(query, limit=20, include_sensitive=False):
    query = query.strip()

    if not query:
        return []

    connection = get_connection()

    try:
        sensitive_filter = ""

        if not include_sensitive:
            sensitive_filter = """
                AND documents.is_sensitive = 0
            """

        rows = connection.execute(f"""
            SELECT
                documents.id,
                documents.path,
                documents.title,
                documents.file_type,
                chunks.content,
                bm25(chunks_fts) AS score
            FROM chunks_fts
            JOIN chunks
                ON chunks.id = chunks_fts.rowid
            JOIN documents
                ON documents.id = chunks.document_id
            WHERE chunks_fts MATCH ?
            {sensitive_filter}
            ORDER BY bm25(chunks_fts)
            LIMIT ?
        """, (query, limit)).fetchall()

        results = {}

        for row in rows:
            document_id = row[0]

            if document_id not in results:
                results[document_id] = row

        return list(results.values())

    except Exception as error:
        print(f"Search error: {error}")
        return []

    finally:
        connection.close()
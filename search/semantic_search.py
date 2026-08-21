import numpy as np

from database.db import get_connection
from search.semantic import generate_embedding
from search.similarity import cosine_similarity


def blob_to_embedding(blob):
    return np.frombuffer(blob, dtype=np.float32)


def make_snippet(content, limit=300):
    content = content.strip()

    if len(content) <= limit:
        return content

    return content[:limit] + "..."


def semantic_search(query, limit=20, include_sensitive=False):
    query = query.strip()

    if not query:
        return []

    query_embedding = generate_embedding(query)

    connection = get_connection()

    try:
        sensitive_filter = ""

        if not include_sensitive:
            sensitive_filter = "AND documents.is_sensitive = 0"

        rows = connection.execute(f"""
            SELECT
                chunks.id,
                documents.id,
                chunks.content,
                documents.path,
                documents.title,
                documents.file_type,
                chunk_embeddings.embedding
            FROM chunk_embeddings
            JOIN chunks
                ON chunks.id = chunk_embeddings.chunk_id
            JOIN documents
                ON documents.id = chunks.document_id
            WHERE 1 = 1
            {sensitive_filter}
        """).fetchall()

        document_results = {}

        for row in rows:
            (
                chunk_id,
                document_id,
                content,
                path,
                title,
                file_type,
                embedding_blob
            ) = row

            embedding = blob_to_embedding(embedding_blob)

            score = cosine_similarity(
                query_embedding,
                embedding
            )

            if (
                document_id not in document_results
                or score > document_results[document_id][5]
            ):
                document_results[document_id] = (
                    document_id,
                    path,
                    title,
                    file_type,
                    make_snippet(content),
                    score
                )

        results = list(document_results.values())

        results.sort(
            key=lambda result: result[5],
            reverse=True
        )

        return results[:limit]

    finally:
        connection.close()
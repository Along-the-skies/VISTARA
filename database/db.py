import sqlite3
from config import DATABASE_PATH
from search.sensitivity import is_sensitive_path

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    connection = get_connection()
    connection.execute("""
    CREATE TABLE IF NOT EXISTS documents (
       id INTEGER PRIMARY KEY,
       path TEXT,
       title TEXT,
       content TEXT,
       file_type TEXT,
       file_size INTEGER,
       created_at TEXT,
       modified_at TEXT,
       indexed_at TEXT,
       content_hash TEXT 
       )    """
        
    )



    connection.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts
        USING fts5(
            title,
            content,
            content='documents',
            content_rowid='id'
        )
    """)

    
    connection.commit()

    connection.execute("""CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);""")

    connection.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
    USING fts5(
        content,
        content='chunks',
        content_rowid='id'
    )
""")

    connection.execute("""
            CREATE TABLE IF NOT EXISTS chunk_embeddings (
                chunk_id INTEGER PRIMARY KEY,
                embedding BLOB NOT NULL,
                FOREIGN KEY (chunk_id) REFERENCES chunks(id)
            )
        """)

    connection.commit()
    connection.close()

def rebuild_fts():
    connection = get_connection()

    try:
        connection.execute("""
            INSERT INTO documents_fts(documents_fts)
            VALUES ('rebuild')
        """)

        connection.execute("""
            INSERT INTO chunks_fts(chunks_fts)
            VALUES ('rebuild')
        """)

        

        connection.commit()

    finally:
        connection.close()


def add_sensitive_column():
    connection = get_connection()

    try:
        connection.execute("""
            ALTER TABLE documents
            ADD COLUMN is_sensitive INTEGER DEFAULT 0
        """)
        connection.commit()
    except sqlite3.OperationalError as Error:
        if "duplicate column name" not in str(Error):
            raise
    finally:
        connection.close()


def mark_sensitive_documents():
    connection = get_connection()
    try:
        rows = connection.execute("""
            SELECT id, path
            FROM documents
        """).fetchall()

        for document_id, path in rows:
            sensitive = 1 if is_sensitive_path(path) else 0

            connection.execute("""
                UPDATE documents
                SET is_sensitive = ?
                WHERE id = ?
            """, (sensitive, document_id))

        connection.commit()
    finally:
        connection.close()
        add_sensitive_column()
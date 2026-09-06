import sqlite3


DB_NAME = "conversations.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_message(session_id: str, role: str, content: str):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
        """,
        (session_id, role, content)
    )

    connection.commit()
    connection.close()


def get_messages(session_id: str):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT role, content
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
        """,
        (session_id,)
    )

    messages = [
        {
            "role": row[0],
            "content": row[1]
        }
        for row in cursor.fetchall()
    ]

    connection.close()

    return messages
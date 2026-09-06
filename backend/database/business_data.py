import sqlite3

DB_NAME = "conversations.db"


def create_business_tables():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            segment TEXT NOT NULL,
            outstanding_amount REAL NOT NULL,
            risk_score REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    existing_count = connection.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]

    if existing_count == 0:
        customers = [
            (1, "Acme Corp", "Enterprise", 185000, 82, "High Risk"),
            (2, "Nova Retail", "SMB", 42000, 35, "Low Risk"),
            (3, "Vertex Ltd", "Enterprise", 127500, 71, "High Risk"),
            (4, "BlueWave Inc", "Mid-Market", 68000, 54, "Medium Risk"),
            (5, "Prime Systems", "Enterprise", 210000, 91, "Critical Risk"),
            (6, "GreenField Co", "SMB", 31500, 28, "Low Risk"),
            (7, "Orbit Solutions", "Mid-Market", 95000, 63, "Medium Risk"),
            (8, "Delta Works", "Enterprise", 156000, 76, "High Risk"),
        ]

        connection.executemany(
            """
            INSERT INTO customers
            (id, name, segment, outstanding_amount, risk_score, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            customers
        )

    connection.commit()
    connection.close()


def get_high_risk_customers(limit=5):
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.execute(
        """
        SELECT
            name,
            segment,
            outstanding_amount,
            risk_score,
            status
        FROM customers
        WHERE risk_score >= 70
        ORDER BY risk_score DESC
        LIMIT ?
        """,
        (limit,)
    )

    results = [
        {
            "name": row[0],
            "segment": row[1],
            "outstanding_amount": row[2],
            "risk_score": row[3],
            "status": row[4],
        }
        for row in cursor.fetchall()
    ]

    connection.close()

    return results
import sqlite3

from backend.database.business_data import DB_NAME


def get_customer_risk_summary(limit: int = 5):
    """
    Retrieve customers with the highest risk scores.
    """

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

    customers = [
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

    return {
        "tool": "customer_risk_summary",
        "customers": customers,
        "count": len(customers),
    }


def get_customer_business_metrics():
    """
    Calculate high-level customer risk and outstanding-balance metrics.
    """

    connection = sqlite3.connect(DB_NAME)

    total_customers = connection.execute(
        """
        SELECT COUNT(*)
        FROM customers
        """
    ).fetchone()[0]

    high_risk_customers = connection.execute(
        """
        SELECT COUNT(*)
        FROM customers
        WHERE risk_score >= 70
        """
    ).fetchone()[0]

    total_outstanding = connection.execute(
        """
        SELECT SUM(outstanding_amount)
        FROM customers
        """
    ).fetchone()[0]

    high_risk_outstanding = connection.execute(
        """
        SELECT SUM(outstanding_amount)
        FROM customers
        WHERE risk_score >= 70
        """
    ).fetchone()[0]

    average_risk = connection.execute(
        """
        SELECT AVG(risk_score)
        FROM customers
        """
    ).fetchone()[0]

    connection.close()

    return {
        "tool": "customer_business_metrics",
        "total_customers": total_customers,
        "high_risk_customers": high_risk_customers,
        "total_outstanding": total_outstanding,
        "high_risk_outstanding": high_risk_outstanding,
        "average_risk_score": round(average_risk, 2),
    }


def get_highest_outstanding_customer():
    """
    Find the customer with the highest outstanding amount.
    """

    connection = sqlite3.connect(DB_NAME)

    row = connection.execute(
        """
        SELECT
            name,
            segment,
            outstanding_amount,
            risk_score,
            status
        FROM customers
        ORDER BY outstanding_amount DESC
        LIMIT 1
        """
    ).fetchone()

    connection.close()

    if not row:
        return {
            "tool": "highest_outstanding_customer",
            "customer": None,
        }

    return {
        "tool": "highest_outstanding_customer",
        "customer": {
            "name": row[0],
            "segment": row[1],
            "outstanding_amount": row[2],
            "risk_score": row[3],
            "status": row[4],
        },
    }
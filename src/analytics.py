from sqlalchemy import text

from database import engine


ANALYTICS_QUERIES = {
    "Total Revenue": """
        SELECT ROUND(
            SUM(oi.quantity * p.price)::numeric,
            2
        ) AS total_revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed';
    """,

    "Average Order Value": """
        SELECT ROUND(
            AVG(order_total)::numeric,
            2
        ) AS average_order_value
        FROM (
            SELECT
                o.order_id,
                SUM(oi.quantity * p.price) AS order_total
            FROM orders o
            JOIN order_items oi
                ON o.order_id = oi.order_id
            JOIN products p
                ON oi.product_id = p.product_id
            WHERE o.status = 'completed'
            GROUP BY o.order_id
        ) order_totals;
    """,

    "Total Units Sold": """
        SELECT SUM(oi.quantity) AS total_units_sold
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed';
    """,

    "Order Status Distribution": """
        SELECT
            status,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY status
        ORDER BY order_count DESC;
    """,

    "Revenue By Category": """
        SELECT
            p.category,
            ROUND(
                SUM(oi.quantity * p.price)::numeric,
                2
            ) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE o.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC;
    """,
}


def run_query(query):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()


def run_analytics():
    print("\n")
    print("=" * 45)
    print("           SQL ANALYTICS")
    print("=" * 45)

    for title, query in ANALYTICS_QUERIES.items():

        print(f"\n{title}")
        print("-" * 35)

        results = run_query(query)

        for row in results:
            print(row)

    print("\n" + "=" * 45)
    print("       ANALYTICS COMPLETED")
    print("=" * 45)


if __name__ == "__main__":
    run_analytics()
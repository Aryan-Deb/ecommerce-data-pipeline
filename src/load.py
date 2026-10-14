import pandas as pd
from sqlalchemy import text

from database import engine
from config import PROCESSED_DATA_DIR

PROCESSED_DIR = PROCESSED_DATA_DIR


def clear_tables():
    print("Clearing existing database tables...")

    with engine.begin() as connection:
        connection.execute(
            text("""
                TRUNCATE TABLE
                    order_items,
                    orders,
                    products,
                    customers
                RESTART IDENTITY CASCADE;
            """)
        )

    print("Database tables cleared successfully.")


def load_table(df, table_name):
    print(f"Loading {table_name}...")

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(f"{len(df)} rows loaded into {table_name}.")


def get_existing_ids(table_name, id_column):
    query = text(
        f"SELECT {id_column} FROM {table_name}"
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        return {
            row[0]
            for row in result.fetchall()
        }


def incremental_load_table(
    df,
    table_name,
    id_column,
):
    existing_ids = get_existing_ids(
        table_name,
        id_column,
    )

    new_rows = df[
        ~df[id_column].isin(existing_ids)
    ].copy()

    if new_rows.empty:
        print(
            f"No new records for {table_name}."
        )
        return 0

    new_rows.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi",
    )

    print(
        f"{len(new_rows)} new rows loaded into "
        f"{table_name}."
    )

    return len(new_rows)


def upsert_table(
    df,
    table_name,
    id_column,
):
    """
    Insert new records and update existing records.
    """

    columns = list(df.columns)

    column_names = ", ".join(
        f'"{column}"'
        for column in columns
    )

    values = ", ".join(
        f":{column}"
        for column in columns
    )

    update_columns = [
        column
        for column in columns
        if column != id_column
    ]

    update_clause = ", ".join(
        f'"{column}" = EXCLUDED."{column}"'
        for column in update_columns
    )

    query = text(
        f"""
        INSERT INTO {table_name} (
            {column_names}
        )
        VALUES (
            {values}
        )
        ON CONFLICT ("{id_column}")
        DO UPDATE SET
            {update_clause};
        """
    )

    records = df.to_dict(
        orient="records"
    )

    if not records:
        return 0

    with engine.begin() as connection:
        connection.execute(
            query,
            records,
        )

    print(
        f"{len(records)} records upserted into "
        f"{table_name}."
    )

    return len(records)


def load_data():
    """
    Full refresh loading.
    """

    print(
        "\nLoading processed data into PostgreSQL..."
    )

    customers = pd.read_csv(
        f"{PROCESSED_DIR}/customers_clean.csv"
    )

    products = pd.read_csv(
        f"{PROCESSED_DIR}/products_clean.csv"
    )

    orders = pd.read_csv(
        f"{PROCESSED_DIR}/orders_clean.csv"
    )

    order_items = pd.read_csv(
        f"{PROCESSED_DIR}/order_items_clean.csv"
    )

    clear_tables()

    load_table(
        customers,
        "customers",
    )

    load_table(
        products,
        "products",
    )

    load_table(
        orders,
        "orders",
    )

    load_table(
        order_items,
        "order_items",
    )

    print(
        "PostgreSQL full refresh completed successfully."
    )


def incremental_load_data():
    """
    Incremental loading using new-record detection.
    """

    print(
        "\nStarting incremental PostgreSQL load..."
    )

    customers = pd.read_csv(
        f"{PROCESSED_DIR}/customers_clean.csv"
    )

    products = pd.read_csv(
        f"{PROCESSED_DIR}/products_clean.csv"
    )

    orders = pd.read_csv(
        f"{PROCESSED_DIR}/orders_clean.csv"
    )

    order_items = pd.read_csv(
        f"{PROCESSED_DIR}/order_items_clean.csv"
    )

    total_new_records = 0

    total_new_records += incremental_load_table(
        customers,
        "customers",
        "customer_id",
    )

    total_new_records += incremental_load_table(
        products,
        "products",
        "product_id",
    )

    total_new_records += incremental_load_table(
        orders,
        "orders",
        "order_id",
    )

    total_new_records += incremental_load_table(
        order_items,
        "order_items",
        "order_item_id",
    )

    print(
        "\nIncremental load completed successfully."
    )

    print(
        f"Total new records loaded: "
        f"{total_new_records}"
    )

    return total_new_records


def upsert_data():
    """
    Incremental loading with INSERT + UPDATE.
    """

    print(
        "\nStarting incremental UPSERT load..."
    )

    customers = pd.read_csv(
        f"{PROCESSED_DIR}/customers_clean.csv"
    )

    products = pd.read_csv(
        f"{PROCESSED_DIR}/products_clean.csv"
    )

    orders = pd.read_csv(
        f"{PROCESSED_DIR}/orders_clean.csv"
    )

    order_items = pd.read_csv(
        f"{PROCESSED_DIR}/order_items_clean.csv"
    )

    total_records = 0

    # Parent tables first
    total_records += upsert_table(
        customers,
        "customers",
        "customer_id",
    )

    total_records += upsert_table(
        products,
        "products",
        "product_id",
    )

    # Child tables after parent tables
    total_records += upsert_table(
        orders,
        "orders",
        "order_id",
    )

    total_records += upsert_table(
        order_items,
        "order_items",
        "order_item_id",
    )

    print(
        "\nIncremental UPSERT completed successfully."
    )

    print(
        f"Total records processed: "
        f"{total_records}"
    )

    return total_records


if __name__ == "__main__":
    load_data()
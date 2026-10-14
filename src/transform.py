import pandas as pd


def transform_customers(df):
    original_rows = len(df)

    df = df.copy()

    df = df.drop_duplicates(
        subset=["customer_id"],
        keep="first",
    )

    df["email"] = (
        df["email"]
        .str.lower()
        .str.strip()
    )

    removed_rows = original_rows - len(df)

    return df, {
        "table": "customers",
        "input_rows": original_rows,
        "output_rows": len(df),
        "removed_rows": removed_rows,
    }


def transform_products(df):
    original_rows = len(df)

    df = df.copy()

    df = df[df["price"] > 0]

    df["category"] = (
        df["category"]
        .str.strip()
        .str.title()
    )

    removed_rows = original_rows - len(df)

    return df, {
        "table": "products",
        "input_rows": original_rows,
        "output_rows": len(df),
        "removed_rows": removed_rows,
    }


def transform_orders(df):
    original_rows = len(df)

    df = df.copy()

    df["status"] = df["status"].fillna("unknown")

    df["status"] = (
        df["status"]
        .str.lower()
        .str.strip()
    )

    return df, {
        "table": "orders",
        "input_rows": original_rows,
        "output_rows": len(df),
        "removed_rows": original_rows - len(df),
    }


def transform_order_items(df, valid_order_ids=None, valid_product_ids=None):
    original_rows = len(df)

    df = df.copy()

    # Remove duplicate order items
    df = df.drop_duplicates(
        subset=["order_item_id"],
        keep="first",
    )

    # Keep only order items whose order still exists
    if valid_order_ids is not None:
        df = df[df["order_id"].isin(valid_order_ids)]

    # Keep only order items whose product still exists
    if valid_product_ids is not None:
        df = df[df["product_id"].isin(valid_product_ids)]

    removed_rows = original_rows - len(df)

    return df, {
        "table": "order_items",
        "input_rows": original_rows,
        "output_rows": len(df),
        "removed_rows": removed_rows,
    }


def print_transformation_summary(reports):
    print("\n")
    print("=" * 45)
    print("       TRANSFORMATION SUMMARY")
    print("=" * 45)

    for report in reports:
        print(f"\n{report['table'].upper()}")
        print("-" * 30)
        print(f"Input rows:   {report['input_rows']}")
        print(f"Output rows:  {report['output_rows']}")
        print(f"Removed rows: {report['removed_rows']}")

    print("\n" + "=" * 45)
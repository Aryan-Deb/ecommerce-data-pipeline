import pandas as pd


def validate_customers(df):
    duplicate_customers = df.duplicated(
        subset=["customer_id"]
    ).sum()

    missing_emails = df["email"].isna().sum()

    report = {
        "table": "customers",
        "raw_rows": len(df),
        "duplicate_customer_ids": duplicate_customers,
        "missing_emails": missing_emails,
    }

    return report


def validate_products(df):
    invalid_prices = (df["price"] <= 0).sum()

    report = {
        "table": "products",
        "raw_rows": len(df),
        "invalid_prices": invalid_prices,
    }

    return report


def validate_orders(df):
    missing_status = df["status"].isna().sum()

    report = {
        "table": "orders",
        "raw_rows": len(df),
        "missing_status": missing_status,
    }

    return report


def validate_order_items(df):
    duplicate_items = df.duplicated(
        subset=["order_item_id"]
    ).sum()

    report = {
        "table": "order_items",
        "raw_rows": len(df),
        "duplicate_order_item_ids": duplicate_items,
    }

    return report


def print_validation_report(reports):
    print("\n")
    print("=" * 45)
    print("           DATA QUALITY REPORT")
    print("=" * 45)

    for report in reports:
        print(f"\n{report['table'].upper()}")
        print("-" * 30)

        for key, value in report.items():
            if key != "table":
                label = key.replace("_", " ").title()
                print(f"{label}: {value}")

    print("\n" + "=" * 45)
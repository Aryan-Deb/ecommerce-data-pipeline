import pandas as pd

from src.validate import (
    validate_customers,
    validate_products,
    validate_orders,
    validate_order_items,
)


def test_validate_customers():
    df = pd.DataFrame({
        "customer_id": [1, 1, 2],
        "email": ["a@test.com", None, "b@test.com"],
    })

    result = validate_customers(df)

    assert result["raw_rows"] == 3
    assert result["duplicate_customer_ids"] == 1
    assert result["missing_emails"] == 1


def test_validate_products():
    df = pd.DataFrame({
        "product_id": [1, 2, 3],
        "price": [100, -20, 50],
    })

    result = validate_products(df)

    assert result["raw_rows"] == 3
    assert result["invalid_prices"] == 1


def test_validate_orders():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "status": ["completed", None],
    })

    result = validate_orders(df)

    assert result["raw_rows"] == 2
    assert result["missing_status"] == 1


def test_validate_order_items():
    df = pd.DataFrame({
        "order_item_id": [1, 1, 2],
    })

    result = validate_order_items(df)

    assert result["raw_rows"] == 3
    assert result["duplicate_order_item_ids"] == 1
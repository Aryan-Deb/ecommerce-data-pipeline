import pandas as pd

from src.transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_order_items,
)


def test_transform_customers_removes_duplicates():
    df = pd.DataFrame({
        "customer_id": [1, 1, 2],
        "email": [
            "A@TEST.COM",
            "duplicate@test.com",
            "B@TEST.COM",
        ],
    })

    result, report = transform_customers(df)

    assert len(result) == 2
    assert report["removed_rows"] == 1
    assert result.iloc[0]["email"] == "a@test.com"


def test_transform_products_removes_invalid_prices():
    df = pd.DataFrame({
        "product_id": [1, 2, 3],
        "product_name": ["A", "B", "C"],
        "category": [" electronics ", "books", "clothing"],
        "price": [100, -20, 50],
    })

    result, report = transform_products(df)

    assert len(result) == 2
    assert report["removed_rows"] == 1


def test_transform_orders_fills_missing_status():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "status": ["completed", None],
    })

    result, report = transform_orders(df)

    assert len(result) == 2
    assert result.iloc[1]["status"] == "unknown"
    assert report["removed_rows"] == 0


def test_transform_order_items_removes_duplicates():
    df = pd.DataFrame({
        "order_item_id": [1, 1, 2],
        "order_id": [10, 10, 20],
        "product_id": [1, 1, 2],
        "quantity": [2, 2, 3],
    })

    result, report = transform_order_items(df)

    assert len(result) == 2
    assert report["removed_rows"] == 1
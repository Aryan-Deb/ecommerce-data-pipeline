import os
import random
from datetime import datetime, timedelta

import pandas as pd


RAW_DATA_DIR = "data/raw"


def generate_customers(num_customers=100):
    cities = [
        "Delhi",
        "Gurgaon",
        "Noida",
        "Mumbai",
        "Bangalore",
        "Hyderabad",
        "Pune",
        "Chennai",
    ]

    customers = []

    for customer_id in range(1, num_customers + 1):
        customers.append(
            {
                "customer_id": customer_id,
                "name": f"Customer {customer_id}",
                "email": f"customer{customer_id}@example.com",
                "city": random.choice(cities),
                "signup_date": (
                    datetime(2025, 1, 1)
                    + timedelta(days=random.randint(0, 365))
                ).date(),
            }
        )

    return pd.DataFrame(customers)


def generate_products(num_products=30):
    categories = [
        "Electronics",
        "Clothing",
        "Home",
        "Books",
        "Sports",
    ]

    products = []

    for product_id in range(1, num_products + 1):
        products.append(
            {
                "product_id": product_id,
                "product_name": f"Product {product_id}",
                "category": random.choice(categories),
                "price": round(random.uniform(10, 1000), 2),
            }
        )

    return pd.DataFrame(products)


def generate_orders(num_orders=500):
    statuses = [
        "completed",
        "completed",
        "completed",
        "cancelled",
        "pending",
    ]

    orders = []

    for order_id in range(1, num_orders + 1):
        order_date = datetime(2025, 1, 1) + timedelta(
            days=random.randint(0, 365)
        )

        orders.append(
            {
                "order_id": order_id,
                "customer_id": random.randint(1, 100),
                "order_date": order_date.date(),
                "status": random.choice(statuses),
            }
        )

    return pd.DataFrame(orders)


def generate_order_items(num_items=1000):
    items = []

    for item_id in range(1, num_items + 1):
        quantity = random.randint(1, 5)

        items.append(
            {
                "order_item_id": item_id,
                "order_id": random.randint(1, 500),
                "product_id": random.randint(1, 30),
                "quantity": quantity,
            }
        )

    return pd.DataFrame(items)


def add_data_quality_issues(customers, products, orders, order_items):
    # Missing customer email
    customers.loc[5, "email"] = None

    # Duplicate customer
    customers = pd.concat(
        [customers, customers.iloc[[10]]],
        ignore_index=True,
    )

    # Invalid product price
    products.loc[3, "price"] = -50

    # Missing order status
    orders.loc[7, "status"] = None

    # Duplicate order item
    order_items = pd.concat(
        [order_items, order_items.iloc[[20]]],
        ignore_index=True,
    )

    return customers, products, orders, order_items


def save_data():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders()
    order_items = generate_order_items()

    customers, products, orders, order_items = add_data_quality_issues(
        customers,
        products,
        orders,
        order_items,
    )

    customers.to_csv(
        f"{RAW_DATA_DIR}/customers.csv",
        index=False,
    )

    products.to_csv(
        f"{RAW_DATA_DIR}/products.csv",
        index=False,
    )

    orders.to_csv(
        f"{RAW_DATA_DIR}/orders.csv",
        index=False,
    )

    order_items.to_csv(
        f"{RAW_DATA_DIR}/order_items.csv",
        index=False,
    )

    print("Raw e-commerce data generated successfully.")


if __name__ == "__main__":
    save_data()
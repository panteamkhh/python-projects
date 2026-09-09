"""
Day 11 - Pandas Fundamentals
Generates a reproducible, realistic-looking retail sales dataset
(data/retail_sales.csv) used by main.py and test_main.py.

Kept as a separate script (instead of shipping a static CSV only)
so the reader can see exactly how the data was produced and can
regenerate or scale it up/down.
"""

import numpy as np
import pandas as pd

RANDOM_SEED = 42
N_ROWS = 600

REGIONS = ["North", "South", "East", "West"]
SEGMENTS = ["Consumer", "Corporate", "Small Business"]

CATEGORIES = {
    "Electronics": ["Wireless Mouse", "Bluetooth Speaker", "USB-C Hub", "Webcam", "Keyboard"],
    "Office Supplies": ["Notebook Pack", "Printer Paper", "Stapler", "Desk Organizer", "Sticky Notes"],
    "Furniture": ["Office Chair", "Standing Desk", "Bookshelf", "Filing Cabinet", "Desk Lamp"],
    "Apparel": ["T-Shirt", "Hoodie", "Cap", "Socks Pack", "Jacket"],
}

BASE_PRICES = {
    "Wireless Mouse": 18.0, "Bluetooth Speaker": 45.0, "USB-C Hub": 32.0,
    "Webcam": 55.0, "Keyboard": 40.0,
    "Notebook Pack": 6.5, "Printer Paper": 8.0, "Stapler": 5.0,
    "Desk Organizer": 12.0, "Sticky Notes": 3.5,
    "Office Chair": 120.0, "Standing Desk": 260.0, "Bookshelf": 95.0,
    "Filing Cabinet": 140.0, "Desk Lamp": 22.0,
    "T-Shirt": 15.0, "Hoodie": 35.0, "Cap": 10.0, "Socks Pack": 8.0, "Jacket": 60.0,
}


def generate_dataset(n_rows: int = N_ROWS, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Build a synthetic but realistic retail sales DataFrame.

    Columns: order_id, order_date, region, customer_segment,
    product_category, product_name, quantity, unit_price, discount, revenue
    """
    rng = np.random.default_rng(seed)

    categories = list(CATEGORIES.keys())
    category_choices = rng.choice(categories, size=n_rows)
    product_names = [rng.choice(CATEGORIES[cat]) for cat in category_choices]
    unit_prices = np.array([BASE_PRICES[p] for p in product_names])

    quantities = rng.integers(1, 8, size=n_rows)
    discounts = rng.choice([0.0, 0.05, 0.1, 0.15, 0.2], size=n_rows, p=[0.5, 0.2, 0.15, 0.1, 0.05])

    dates = pd.to_datetime("2024-01-01") + pd.to_timedelta(
        rng.integers(0, 365, size=n_rows), unit="D"
    )

    revenue = (unit_prices * quantities) * (1 - discounts)

    df = pd.DataFrame({
        "order_id": [f"ORD-{i:05d}" for i in range(1, n_rows + 1)],
        "order_date": dates,
        "region": rng.choice(REGIONS, size=n_rows),
        "customer_segment": rng.choice(SEGMENTS, size=n_rows, p=[0.55, 0.30, 0.15]),
        "product_category": category_choices,
        "product_name": product_names,
        "quantity": quantities,
        "unit_price": unit_prices.round(2),
        "discount": discounts,
        "revenue": revenue.round(2),
    })

    return df.sort_values("order_date").reset_index(drop=True)


if __name__ == "__main__":
    dataset = generate_dataset()
    dataset.to_csv("data/retail_sales.csv", index=False)
    print(f"Wrote {len(dataset)} rows to data/retail_sales.csv")

"""
Day 11 - Pandas Fundamentals

A small but realistic sales-analysis tool built on top of a single
retail_sales.csv file. The goal of this project is not "print a
DataFrame" but to answer concrete business questions with pandas:

- How much revenue did we make, and how is it trending month over month?
- Which regions / product categories / products drive the most revenue?
- How does the average order value differ across customer segments?
- Where should the business focus next?

Run directly for a printed console report:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class SalesAnalyzer:
    """Loads a retail sales CSV and answers common business questions on it."""

    REQUIRED_COLUMNS = {
        "order_id", "order_date", "region", "customer_segment",
        "product_category", "product_name", "quantity", "unit_price",
        "discount", "revenue",
    }

    def __init__(self, csv_path: str | Path = "data/retail_sales.csv") -> None:
        self.csv_path = Path(csv_path)
        self.df: pd.DataFrame = self._load()

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def _load(self) -> pd.DataFrame:
        """Read the CSV, validate its shape, and parse dates."""
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {self.csv_path}. "
                "Run `python generate_data.py` first."
            )

        df = pd.read_csv(self.csv_path, parse_dates=["order_date"])

        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Dataset is missing expected columns: {missing}")

        return df

    # ------------------------------------------------------------------
    # Basic overview
    # ------------------------------------------------------------------
    def overview(self) -> dict:
        """High-level summary: row count, date range, total revenue."""
        return {
            "total_orders": len(self.df),
            "date_range": (
                self.df["order_date"].min().date(),
                self.df["order_date"].max().date(),
            ),
            "total_revenue": round(self.df["revenue"].sum(), 2),
            "average_order_value": round(self.df["revenue"].mean(), 2),
        }

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------
    def revenue_by_region(self) -> pd.Series:
        """Total revenue per region, sorted descending."""
        return (
            self.df.groupby("region")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .round(2)
        )

    def revenue_by_category(self) -> pd.Series:
        """Total revenue per product category, sorted descending."""
        return (
            self.df.groupby("product_category")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .round(2)
        )

    def top_products(self, n: int = 5) -> pd.DataFrame:
        """Top-n products by total revenue, with units sold."""
        summary = (
            self.df.groupby("product_name")
            .agg(units_sold=("quantity", "sum"), total_revenue=("revenue", "sum"))
            .sort_values("total_revenue", ascending=False)
            .round(2)
        )
        return summary.head(n)

    def average_order_value_by_segment(self) -> pd.Series:
        """Average order value (revenue per order) per customer segment."""
        return (
            self.df.groupby("customer_segment")["revenue"]
            .mean()
            .sort_values(ascending=False)
            .round(2)
        )

    def monthly_revenue_trend(self) -> pd.Series:
        """Total revenue per calendar month, in chronological order."""
        monthly = self.df.set_index("order_date")["revenue"].resample("ME").sum()
        monthly.index = monthly.index.strftime("%Y-%m")
        return monthly.round(2)

    def filter_orders(
        self,
        region: str | None = None,
        category: str | None = None,
        min_revenue: float | None = None,
    ) -> pd.DataFrame:
        """Return a filtered slice of the raw orders (illustrates boolean indexing)."""
        result = self.df

        if region is not None:
            result = result[result["region"] == region]
        if category is not None:
            result = result[result["product_category"] == category]
        if min_revenue is not None:
            result = result[result["revenue"] >= min_revenue]

        return result

    # ------------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------------
    def print_report(self) -> None:
        """Print a readable console report covering all analyses above."""
        overview = self.overview()

        print("=" * 60)
        print("RETAIL SALES REPORT")
        print("=" * 60)
        print(f"Orders analyzed : {overview['total_orders']}")
        print(f"Date range      : {overview['date_range'][0]} -> {overview['date_range'][1]}")
        print(f"Total revenue   : ${overview['total_revenue']:,}")
        print(f"Avg order value : ${overview['average_order_value']:,}")

        print("\nRevenue by region:")
        print(self.revenue_by_region().to_string())

        print("\nRevenue by category:")
        print(self.revenue_by_category().to_string())

        print("\nTop 5 products by revenue:")
        print(self.top_products(5).to_string())

        print("\nAverage order value by customer segment:")
        print(self.average_order_value_by_segment().to_string())

        print("\nMonthly revenue trend:")
        print(self.monthly_revenue_trend().to_string())
        print("=" * 60)


if __name__ == "__main__":
    analyzer = SalesAnalyzer()
    analyzer.print_report()

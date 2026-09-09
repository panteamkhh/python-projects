"""
Day 12 - Data Cleaning Pipeline

Real analysis is only as good as the data behind it, and real data is
rarely clean. This project turns a messy customer-orders CSV into an
analysis-ready DataFrame, and — just as importantly — reports exactly
what was fixed along the way.

Run directly for a before/after cleaning report:
    python main.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


class DataCleaner:
    """Loads a messy orders CSV and produces a clean, analysis-ready DataFrame."""

    def __init__(self, csv_path: str | Path = "data/raw_customer_orders.csv") -> None:
        self.csv_path = Path(csv_path)
        self.raw_df: pd.DataFrame = self._load_raw()
        self.clean_df: pd.DataFrame | None = None
        self.report: dict = {}

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------
    def _load_raw(self) -> pd.DataFrame:
        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {self.csv_path}. "
                "Run `python generate_data.py` first."
            )
        return pd.read_csv(self.csv_path)

    # ------------------------------------------------------------------
    # Individual cleaning steps (each one is independently testable)
    # ------------------------------------------------------------------
    @staticmethod
    def standardize_text(series: pd.Series) -> pd.Series:
        """Strip whitespace and normalize casing to Title Case."""
        return series.astype(str).str.strip().str.title().replace("Nan", np.nan)

    @staticmethod
    def parse_messy_dates(series: pd.Series) -> pd.Series:
        """Parse a column containing multiple date string formats."""
        return pd.to_datetime(series, format="mixed", errors="coerce")

    @staticmethod
    def parse_messy_amount(series: pd.Series) -> pd.Series:
        """Strip currency symbols, commas, and whitespace; convert to float."""
        cleaned = (
            series.astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        return pd.to_numeric(cleaned, errors="coerce")

    @staticmethod
    def parse_quantity(series: pd.Series) -> pd.Series:
        """Convert quantity to numeric, turning junk strings into NaN."""
        return pd.to_numeric(series, errors="coerce")

    # ------------------------------------------------------------------
    # Full pipeline
    # ------------------------------------------------------------------
    def clean(self) -> pd.DataFrame:
        """Run the full cleaning pipeline and store a step-by-step report."""
        df = self.raw_df.copy()
        report = {"initial_rows": len(df)}

        # 1. Remove exact duplicate rows
        before = len(df)
        df = df.drop_duplicates()
        report["duplicates_removed"] = before - len(df)

        # 2. Standardize text columns
        df["customer_name"] = self.standardize_text(df["customer_name"])
        df["region"] = self.standardize_text(df["region"])

        # 3. Parse dates and amounts out of inconsistent string formats
        df["order_date"] = self.parse_messy_dates(df["order_date"])
        df["amount"] = self.parse_messy_amount(df["amount"])
        df["quantity"] = self.parse_quantity(df["quantity"])

        # 4. Drop rows with invalid (non-positive or unparsable) quantity
        before = len(df)
        df = df[df["quantity"].notna() & (df["quantity"] > 0)]
        report["invalid_quantity_rows_removed"] = before - len(df)

        # 5. Handle remaining missing values in critical columns
        before = len(df)
        df = df.dropna(subset=["customer_name", "region", "amount", "order_date"])
        report["missing_value_rows_removed"] = before - len(df)

        df["quantity"] = df["quantity"].astype(int)
        df = df.reset_index(drop=True)

        report["final_rows"] = len(df)
        report["rows_dropped_total"] = report["initial_rows"] - report["final_rows"]

        self.clean_df = df
        self.report = report
        return df

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------
    def save_clean(self, path: str | Path = "data/clean_customer_orders.csv") -> None:
        if self.clean_df is None:
            raise RuntimeError("Call clean() before save_clean().")
        self.clean_df.to_csv(path, index=False)

    def print_report(self) -> None:
        if not self.report:
            self.clean()

        print("=" * 60)
        print("DATA CLEANING REPORT")
        print("=" * 60)
        print(f"Initial rows                 : {self.report['initial_rows']}")
        print(f"Duplicates removed            : {self.report['duplicates_removed']}")
        print(f"Invalid quantity rows removed : {self.report['invalid_quantity_rows_removed']}")
        print(f"Missing-value rows removed    : {self.report['missing_value_rows_removed']}")
        print(f"Final rows                   : {self.report['final_rows']}")
        print(f"Total rows dropped            : {self.report['rows_dropped_total']}")
        print("\nClean dtypes:")
        print(self.clean_df.dtypes.to_string())
        print("\nSample of cleaned data:")
        print(self.clean_df.head(5).to_string(index=False))
        print("=" * 60)


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean()
    cleaner.print_report()
    cleaner.save_clean()
    print("\nSaved cleaned dataset to data/clean_customer_orders.csv")

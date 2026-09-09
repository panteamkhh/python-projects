"""Unit tests for SalesAnalyzer (Day 11 - Pandas Fundamentals)."""

import pandas as pd
import pytest

from generate_data import generate_dataset
from main import SalesAnalyzer


@pytest.fixture
def analyzer(tmp_path) -> SalesAnalyzer:
    """A SalesAnalyzer built on a small, deterministic dataset."""
    csv_path = tmp_path / "retail_sales.csv"
    generate_dataset(n_rows=100, seed=1).to_csv(csv_path, index=False)
    return SalesAnalyzer(csv_path=csv_path)


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        SalesAnalyzer(csv_path=tmp_path / "does_not_exist.csv")


def test_missing_columns_raises(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    pd.DataFrame({"order_id": ["ORD-1"], "revenue": [10.0]}).to_csv(bad_csv, index=False)

    with pytest.raises(ValueError):
        SalesAnalyzer(csv_path=bad_csv)


def test_overview_keys_and_types(analyzer):
    overview = analyzer.overview()
    assert overview["total_orders"] == 100
    assert isinstance(overview["total_revenue"], float)
    assert overview["total_revenue"] > 0


def test_revenue_by_region_sums_to_total(analyzer):
    by_region = analyzer.revenue_by_region()
    total = analyzer.overview()["total_revenue"]
    assert round(by_region.sum(), 2) == round(total, 2)


def test_revenue_by_region_sorted_descending(analyzer):
    by_region = analyzer.revenue_by_region()
    assert list(by_region) == sorted(by_region, reverse=True)


def test_top_products_respects_n(analyzer):
    top3 = analyzer.top_products(n=3)
    assert len(top3) == 3
    assert list(top3.columns) == ["units_sold", "total_revenue"]
    # Sorted descending by total_revenue
    assert list(top3["total_revenue"]) == sorted(top3["total_revenue"], reverse=True)


def test_average_order_value_by_segment_nonempty(analyzer):
    avg_by_segment = analyzer.average_order_value_by_segment()
    assert len(avg_by_segment) > 0
    assert (avg_by_segment > 0).all()


def test_monthly_revenue_trend_is_chronological(analyzer):
    trend = analyzer.monthly_revenue_trend()
    assert list(trend.index) == sorted(trend.index)


def test_filter_orders_by_region(analyzer):
    region = analyzer.df["region"].iloc[0]
    filtered = analyzer.filter_orders(region=region)
    assert (filtered["region"] == region).all()
    assert len(filtered) <= len(analyzer.df)


def test_filter_orders_by_min_revenue(analyzer):
    filtered = analyzer.filter_orders(min_revenue=100)
    assert (filtered["revenue"] >= 100).all()


def test_filter_orders_combined_filters(analyzer):
    region = analyzer.df["region"].iloc[0]
    category = analyzer.df["product_category"].iloc[0]
    filtered = analyzer.filter_orders(region=region, category=category)
    assert (filtered["region"] == region).all()
    assert (filtered["product_category"] == category).all()

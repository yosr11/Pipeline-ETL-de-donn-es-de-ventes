import pandas as pd

def test_silver_quality():
    df = pd.read_parquet("data/silver/sales")
    assert df["order_id"].notna().all()
    assert (df["sales"] > 0).all()
    assert not df.duplicated(["order_id", "product_id"]).any()

def test_gold_total_matches_silver():
    silver = pd.read_parquet("data/silver/sales")
    fact = pd.read_parquet("data/gold/fact_sales")
    assert abs(silver["sales"].sum() - fact["sales"].sum()) < 1
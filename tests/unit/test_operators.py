"""
Unit Tests: Vectorized Transformation Operators
"""

import pandas as pd
import pytest
from data_engine.transformation.operators import (
    AggregateOperator,
    CalculatedColumnOperator,
    CastColumnsOperator,
    CastTypesOperator,
    ConditionalColumnOperator,
    DeduplicateOperator,
    DropColumnsOperator,
    FilterRowsOperator,
    JoinDataFramesOperator,
    NormalizeStringsOperator,
    RenameColumnsOperator,
    SelectColumnsOperator,
    SortOperator,
    SortRowsOperator,
)


def test_select_and_rename_operators():
    df = pd.DataFrame([
        {"id": 1, "raw_name": "Alice", "age": 28, "unused": "xyz"},
        {"id": 2, "raw_name": "Bob", "age": 34, "unused": "abc"},
    ])

    sel_op = SelectColumnsOperator(columns=["id", "raw_name", "age"])
    df1 = sel_op.transform(df)
    assert list(df1.columns) == ["id", "raw_name", "age"]

    ren_op = RenameColumnsOperator(mapping={"raw_name": "customer_name"})
    df2 = ren_op.transform(df1)
    assert list(df2.columns) == ["id", "customer_name", "age"]


def test_deduplicate_and_normalize_operators():
    df = pd.DataFrame([
        {"id": "101", "name": "  ALICE SMITH  ", "email": "ALICE@EXAMPLE.COM"},
        {"id": "101", "name": "alice smith", "email": "alice@example.com"},
        {"id": "102", "name": "  bob jones ", "email": "bob@example.com"},
    ])

    dedup_op = DeduplicateOperator(subset=["id"], keep="first")
    df_dedup = dedup_op.transform(df)
    assert len(df_dedup) == 2

    norm_op = NormalizeStringsOperator(columns=["name"], case_mode="title", strip_whitespace=True)
    df_norm = norm_op.transform(df_dedup)
    assert df_norm.iloc[0]["name"] == "Alice Smith"
    assert df_norm.iloc[1]["name"] == "Bob Jones"


def test_filter_and_calculated_column():
    df = pd.DataFrame([
        {"product": "Laptop", "price": 1200, "quantity": 2},
        {"product": "Mouse", "price": 25, "quantity": 10},
        {"product": "Cable", "price": 10, "quantity": 0},
    ])

    filter_op = FilterRowsOperator(condition_expr="quantity > 0")
    df_filtered = filter_op.transform(df)
    assert len(df_filtered) == 2

    calc_op = CalculatedColumnOperator(new_column_name="total_cost", expression="price * quantity")
    df_calc = calc_op.transform(df_filtered)
    assert "total_cost" in df_calc.columns
    assert df_calc.iloc[0]["total_cost"] == 2400
    assert df_calc.iloc[1]["total_cost"] == 250


def test_aggregate_operator():
    df = pd.DataFrame([
        {"department": "Sales", "salary": 50000},
        {"department": "Sales", "salary": 70000},
        {"department": "Engineering", "salary": 120000},
        {"department": "Engineering", "salary": 140000},
    ])

    agg_op = AggregateOperator(group_by=["department"], aggregations={"salary": "sum"})
    df_agg = agg_op.transform(df)
    assert len(df_agg) == 2
    sales_total = df_agg[df_agg["department"] == "Sales"]["salary"].values[0]
    eng_total = df_agg[df_agg["department"] == "Engineering"]["salary"].values[0]
    assert sales_total == 120000
    assert eng_total == 260000

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence, Tuple

import pandas as pd


COLUMNS_EXPECTED = [
    "transaction_id",
    "date",
    "amount",
    "category",
    "merchant",
    "payment_method",
    "account_type",
    "transaction_type",
    "description",
]


def load_transactions(path: Path | str) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = [c for c in COLUMNS_EXPECTED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).copy()

    # Normalize text columns
    for col in ["category", "merchant", "payment_method", "account_type", "transaction_type"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # Derived columns
    df["date_only"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["weekday"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour

    return df


def apply_filters(
    df: pd.DataFrame,
    *,
    date_range: Tuple[pd.Timestamp, pd.Timestamp] | Tuple | Sequence | None = None,
    categories: Optional[Sequence[str]] = None,
    merchants: Optional[Sequence[str]] = None,
    payment_methods: Optional[Sequence[str]] = None,
    account_types: Optional[Sequence[str]] = None,
) -> pd.DataFrame:
    mask = pd.Series(True, index=df.index)

    if date_range and len(date_range) == 2:
        start, end = date_range
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        mask &= (df["date"] >= start) & (df["date"] <= end + pd.Timedelta(days=1))

    if categories:
        mask &= df["category"].isin(categories)
    if merchants:
        mask &= df["merchant"].isin(merchants)
    if payment_methods:
        mask &= df["payment_method"].isin(payment_methods)
    if account_types:
        mask &= df["account_type"].isin(account_types)

    return df.loc[mask].copy()


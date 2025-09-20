from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import streamlit as st


def kpi_cards(df: pd.DataFrame) -> None:
    total_amount = float(df["amount"].sum()) if not df.empty else 0.0
    num_tx = int(df.shape[0])
    avg_amount = float(df["amount"].mean()) if not df.empty else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Amount", f"${total_amount:,.2f}")
    c2.metric("# Transactions", f"{num_tx:,}")
    c3.metric("Average Amount", f"${avg_amount:,.2f}")


def plot_amount_over_time(df: pd.DataFrame):
    if df.empty:
        return px.line(title="Amount Over Time")
    ts = df.groupby("date_only", as_index=False)["amount"].sum()
    fig = px.line(ts, x="date_only", y="amount", title="Amount Over Time")
    fig.update_traces(mode="lines+markers")
    return fig


def plot_category_breakdown(df: pd.DataFrame):
    if df.empty:
        return px.bar(title="Category Breakdown")
    agg = df.groupby("category", as_index=False)["amount"].sum()
    fig = px.bar(agg, x="category", y="amount", title="Category Breakdown", text_auto=".2s")
    fig.update_layout(xaxis=dict(categoryorder="total descending"))
    return fig


def plot_top_merchants(df: pd.DataFrame, top_n: int = 15):
    if df.empty:
        return px.bar(title="Top Merchants")
    agg = df.groupby("merchant", as_index=False)["amount"].sum().head(top_n)
    fig = px.bar(agg, x="merchant", y="amount", title=f"Top {top_n} Merchants", text_auto=".2s")
    fig.update_layout(xaxis=dict(categoryorder="total descending"))
    return fig


def plot_payment_method_share(df: pd.DataFrame):
    if df.empty:
        return px.pie(title="Payment Method Share")
    agg = df.groupby("payment_method", as_index=False)["amount"].sum()
    fig = px.pie(agg, names="payment_method", values="amount", title="Payment Method Share", hole=0.4)
    return fig


def plot_weekday_hour_heatmap(df: pd.DataFrame):
    if df.empty:
        return px.imshow([[0]], title="Weekday-Hour Heatmap")
    pivot = (
        df.assign(weekday_num=df["date"].dt.weekday)
        .groupby(["weekday_num", "hour"], as_index=False)["amount"].sum()
        .pivot(index="weekday_num", columns="hour", values="amount")
        .reindex(range(7))
        .fillna(0)
    )
    fig = px.imshow(
        pivot.values,
        labels=dict(x="Hour", y="Weekday", color="Amount"),
        x=pivot.columns,
        y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        title="Weekday-Hour Heatmap",
        aspect="auto",
        color_continuous_scale="Blues",
    )
    return fig


def plot_outliers_scatter(df: pd.DataFrame):
    if df.empty:
        return px.scatter(title="Outliers (Z-score)")
    fig = px.scatter(
        df,
        x="date",
        y="amount",
        color="is_outlier",
        color_discrete_map={False: "#1f77b4", True: "#d62728"},
        hover_data=["transaction_id", "category", "merchant", "zscore"],
        title="Outliers by Amount (Z-score)",
    )
    return fig


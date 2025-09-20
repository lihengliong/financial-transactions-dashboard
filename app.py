import pathlib
from datetime import datetime
from typing import Optional

import pandas as pd
import streamlit as st

from src.data import load_transactions, apply_filters
from src.viz import (
    kpi_cards,
    plot_amount_over_time,
    plot_category_breakdown,
    plot_top_merchants,
    plot_payment_method_share,
    plot_weekday_hour_heatmap,
    plot_outliers_scatter,
)
from src.outliers import detect_outliers, OutlierConfig

st.set_page_config(page_title="Financial Transactions Dashboard", layout="wide")

DATA_PATH = pathlib.Path(__file__).parent / "financial_transactions.csv"

@st.cache_data(show_spinner=False)
def get_data() -> pd.DataFrame:
    return load_transactions(DATA_PATH)


def sidebar_filters(df: pd.DataFrame) -> dict:
    st.sidebar.header("Filters")
    min_date = pd.to_datetime(df["date"]).min().date()
    max_date = pd.to_datetime(df["date"]).max().date()
    date_range = st.sidebar.date_input("Date range", (min_date, max_date))

    categories = sorted(df["category"].dropna().unique().tolist())
    merchants = sorted(df["merchant"].dropna().unique().tolist())
    payment_methods = sorted(df["payment_method"].dropna().unique().tolist())
    account_types = sorted(df["account_type"].dropna().unique().tolist())

    selected_categories = st.sidebar.multiselect("Category", categories)
    selected_merchants = st.sidebar.multiselect("Merchant", merchants)
    selected_payment_methods = st.sidebar.multiselect("Payment Method", payment_methods)
    selected_account_types = st.sidebar.multiselect("Account Type", account_types)

    return {
        "date_range": date_range,
        "categories": selected_categories,
        "merchants": selected_merchants,
        "payment_methods": selected_payment_methods,
        "account_types": selected_account_types,
    }


def main():
    st.title("Financial Transactions Dashboard")
    df = get_data()

    filters = sidebar_filters(df)
    df_f = apply_filters(
        df,
        date_range=filters["date_range"],
        categories=filters["categories"],
        merchants=filters["merchants"],
        payment_methods=filters["payment_methods"],
        account_types=filters["account_types"],
    )

    kpi_cards(df_f)

    tab1, tab2, tab3, tab4 = st.tabs(["Time Series", "Breakdowns", "Heatmap", "Outliers"])

    with tab1:
        st.plotly_chart(plot_amount_over_time(df_f), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(plot_category_breakdown(df_f), use_container_width=True)
        with c2:
            st.plotly_chart(plot_payment_method_share(df_f), use_container_width=True)
        
        # Top merchants chart with customizable n
        max_merchants = len(df_f["merchant"].unique()) if not df_f.empty else 1
        col1, col2 = st.columns([4, 1])
        with col1:
            top_n_merchants = st.number_input("Number of top merchants to show", min_value=1, max_value=max_merchants, value=min(15, max_merchants), step=1, key="top_n_merchants")
        with col2:
            st.write("")  # Empty space for alignment
        st.plotly_chart(plot_top_merchants(df_f, top_n=top_n_merchants), use_container_width=True)

    with tab3:
        st.plotly_chart(plot_weekday_hour_heatmap(df_f), use_container_width=True)

    with tab4:
        z_thresh = st.slider("Z-score threshold", 2.0, 5.0, 3.0, 0.1)
        df_out = detect_outliers(df_f, OutlierConfig(zscore_threshold=z_thresh))
        st.plotly_chart(plot_outliers_scatter(df_out), use_container_width=True)
        st.dataframe(df_out[df_out["is_outlier"]].sort_values("zscore", key=abs, ascending=False), use_container_width=True)

    with st.expander("Raw Data"):
        st.dataframe(df_f, use_container_width=True)


if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="Walmart Analytical Suite", layout="wide")

def load_warehouse_data() -> pd.DataFrame:
    """Safely opens connections to extract production tables from SQLite workspace."""
    db_file = Path(__file__).resolve().parent / "data" / "sales.db"
    if not db_file.exists():
        st.error(f"Database instance missing at {db_file}. Run 'python main.py' to generate.")
        st.stop()
    with sqlite3.connect(db_file) as conn:
        df = pd.read_sql_query("SELECT * FROM sales_summary", conn)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

# Data Initialization
df = load_warehouse_data()

# App Header Layout
st.title("Walmart Sales Intelligence Matrix")
st.markdown("Interactive platform visualizing analytical thresholds, rolling 7-day moving averages, and seasonal trends.")
st.markdown("---")

# Top KPIs Matrix
st.header("Executive Core Performance Indicators")
total_revenue = df["Weekly_Sales"].sum()
store_group = df.groupby("Store")["Weekly_Sales"].sum()
top_store_id = store_group.idxmax()
worst_store_id = store_group.idxmin()

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
kpi_col1.metric("Total Enterprise Revenue", f"${total_revenue:,.2f}")
kpi_col2.metric("Top Strategic Store Unit", f"Store {top_store_id}")
kpi_col3.metric("Underperforming Store Unit", f"Store {worst_store_id}")
st.markdown("---")

# Defensive: ensure required analytic columns exist
if "ma7" not in df.columns:
    df = df.sort_values(["Store", "Date"]).reset_index(drop=True)
    df["ma7"] = df.groupby("Store")["Weekly_Sales"].rolling(window=7, min_periods=1).mean().reset_index(level=0, drop=True)
if "trend" not in df.columns:
    df = df.sort_values(["Store", "Date"]).reset_index(drop=True)
    df["sales_diff"] = df.groupby("Store")["Weekly_Sales"].diff()
    df["trend"] = df["sales_diff"].apply(lambda x: "increasing" if x > 0 else ("decreasing" if x < 0 else "stable"))
    df.drop(columns=["sales_diff"], inplace=True)

# Interactive Split Row layout
viz_col1, viz_col2 = st.columns([2, 1])

with viz_col1:
    st.header("Store-Level Rolling Trends")
    selected_store = st.selectbox("Select Target Fleet Store Identifier", sorted(df["Store"].unique()))
    store_mask = df[df["Store"] == selected_store].sort_values("Date")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(store_mask["Date"], store_mask["Weekly_Sales"], alpha=0.4, label="Raw Transacted Sales Value", marker='o')
    ax.plot(store_mask["Date"], store_mask["ma7"], linewidth=3, color='orange', label="Rolling 7-Period MA")
    ax.set_ylabel("Sales Volume ($)")
    ax.legend(facecolor='white', frameon=True)
    st.pyplot(fig)

with viz_col2:
    st.header("Shift Trends Breakdown")
    trend_mix = df["trend"].value_counts()
    fig_pie, ax_pie = plt.subplots(figsize=(5, 5))
    ax_pie.pie(trend_mix.values, labels=trend_mix.index, autopct="%1.1f%%", colors=['#4CAF50','#FF5722'])
    st.pyplot(fig_pie)
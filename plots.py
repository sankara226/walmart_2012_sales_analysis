import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def compile_analytical_plots(df: pd.DataFrame, output_dir: Path):
    """Generates corporate plots and exports artifacts to asset folder location."""
    output_dir.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Global MA7 Performance
    plt.figure(figsize=(10, 5))
    for store in df["Store"].unique():
        subset = df[df["Store"] == store]
        plt.plot(subset["Date"], subset["Weekly_Sales"], alpha=0.15, color='gray')
        plt.plot(subset["Date"], subset["ma7"], alpha=0.7, linewidth=1.5)
    plt.title("Weekly Sales Distributions + Moving Average (7-Day window)")
    plt.tight_layout()
    plt.savefig(output_dir / "weekly_sales_ma7.png")
    plt.close()

    # Chart 2: Store Ranking Performance
    plt.figure(figsize=(10, 5))
    store_sales = df.groupby("Store")["Weekly_Sales"].sum().sort_values(ascending=False)
    sns.barplot(x=store_sales.index, y=store_sales.values, order=store_sales.index, palette="Blues_r")
    plt.title("Aggregated Store Sales Volumetric Summary")
    plt.tight_layout()
    plt.savefig(output_dir / "total_sales_per_store.png")
    plt.close()

    # Chart 3: Seasonality Heatmap
    plt.figure(figsize=(8, 5))
    pivot = df.pivot_table(values="Weekly_Sales", index="Month", columns="Year", aggfunc="sum")
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues", cbar=True)
    plt.title("Strategic Matrix Grid Seasonality Map (Month x Year)")
    plt.tight_layout()
    plt.savefig(output_dir / "sales_heatmap_month_by_year.png")
    plt.close()

    # Chart 4: Categorical Value Distributions (Pie Trend)
    plt.figure(figsize=(6, 6))
    trend_counts = df["trend"].value_counts()
    plt.pie(trend_counts.values, labels=trend_counts.index, autopct="%1.1f%%", colors=['#66b3ff','#ff9999'])
    plt.title("Macro Shift Status Proportional Breakdown")
    plt.tight_layout()
    plt.savefig(output_dir / "trend_summary.png")
    plt.close()
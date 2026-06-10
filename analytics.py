import pandas as pd

def generate_insights(df: pd.DataFrame) -> dict:
    """Aggregates processing values into structured insight dictionary indices."""
    store_totals = df.groupby("Store")["Weekly_Sales"].sum()
    
    best_day_row = df.loc[df["Weekly_Sales"].idxmax()]
    worst_day_row = df.loc[df["Weekly_Sales"].idxmin()]
    
    return {
        "top_store": int(store_totals.idxmax()),
        "worst_store": int(store_totals.idxmin()),
        "trend_summary": df["trend"].value_counts().to_dict(),
        "best_day": {
            "date": best_day_row["Date"].strftime('%Y-%m-%d'),
            "store": int(best_day_row["Store"]),
            "sales": float(best_day_row["Weekly_Sales"])
        },
        "worst_day": {
            "date": worst_day_row["Date"].strftime('%Y-%m-%d'),
            "store": int(worst_day_row["Store"]),
            "sales": float(worst_day_row["Weekly_Sales"])
        }
    }
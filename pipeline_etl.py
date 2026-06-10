import os
import sqlite3
import pandas as pd
import kagglehub
from pathlib import Path


def extract_sales(dataset_name: str = "mikhail1681/walmart-sales", days: int = 30) -> pd.DataFrame:
    """Downloads the official dataset from KaggleHub and filters the most recent transactional matrix.

    To avoid repeated downloads, this function will look for a cached CSV at
    `data/sales_snapshot.csv` in the repository root. If present it will be used
    as the data source. Otherwise the dataset is downloaded and the CSV cache
    is written for future runs.
    """
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    snapshot_path = data_dir / "sales_snapshot.csv"

    if snapshot_path.exists():
        df = pd.read_csv(snapshot_path, parse_dates=["Date"])
    else:
        path = kagglehub.dataset_download(dataset_name)
        files = os.listdir(path)
        csv_files = [f for f in files if f.endswith(".csv")]

        if not csv_files:
            raise FileNotFoundError("No CSV file found in downloaded Kaggle archive workspace.")

        df = pd.read_csv(Path(path) / csv_files[0])
        # normalize date parsing
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

        # persist a snapshot for offline/fast runs
        data_dir.mkdir(parents=True, exist_ok=True)
        try:
            df.to_csv(snapshot_path, index=False)
        except Exception:
            # If writing fails, continue without caching
            pass

    # Ensure Date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
        df["Date"] = pd.to_datetime(df["Date"])

    # Slice the last N days safely
    max_date = df["Date"].max()
    filtered_df = df[df["Date"] >= max_date - pd.Timedelta(days=days)].copy()
    return filtered_df.sort_values(["Store", "Date"]).reset_index(drop=True)

def transform_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Executes rolling transformations, trend indicators, and structural date parsing."""
    # Ensure correct sorting prior to structural groupby operations
    df = df.sort_values(["Store", "Date"]).reset_index(drop=True)
    
    # Calculate 7-period Moving Average
    df["ma7"] = (
        df.groupby("Store")["Weekly_Sales"]
        .rolling(window=7, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )
    
    # Compute clear categorical structural trends
    df["sales_diff"] = df.groupby("Store")["Weekly_Sales"].diff()
    df["trend"] = df["sales_diff"].apply(lambda x: "increasing" if x > 0 else "decreasing")
    df.drop(columns=["sales_diff"], inplace=True)
    
    # Component extraction
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    
    return df

def load_sales_summary(df: pd.DataFrame, db_path: Path, table_name: str = "sales_summary") -> bool:
    """Safely streams structured DataFrames directly into local SQLite relational instances."""
    db_path.parent.mkdir(exist_ok=True)
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to stream transactions to database table {table_name}: {e}")
        return False
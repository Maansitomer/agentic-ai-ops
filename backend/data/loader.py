import pandas as pd
from pathlib import Path


def load_customer_data() -> pd.DataFrame:
    """
    Loads customer usage dataset using the exact file name.
    """

    project_root = Path(__file__).resolve().parents[2]

    data_path = (
        project_root
        / "backend"
        / "data"
        / "customer_usage - customer_usage.csv"
    )

    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {data_path}")

    df = pd.read_csv(data_path)
    return df

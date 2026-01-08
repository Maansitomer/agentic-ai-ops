import numpy as np
import pandas as pd


def make_json_safe(obj):
    """
    Recursively converts numpy / pandas objects to native Python types
    """

    if isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [make_json_safe(v) for v in obj]

    if isinstance(obj, (np.integer,)):
        return int(obj)

    if isinstance(obj, (np.floating,)):
        return float(obj)

    if isinstance(obj, (np.ndarray,)):
        return obj.tolist()

    if isinstance(obj, (pd.Timestamp,)):
        return obj.isoformat()

    return obj

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pandas as pd


@dataclass
class OutlierConfig:
    zscore_threshold: float = 3.0


def detect_outliers(df: pd.DataFrame, config: OutlierConfig | None = None) -> pd.DataFrame:
    if config is None:
        config = OutlierConfig()
    result = df.copy()
    if result.empty:
        result["zscore"] = []
        result["is_outlier"] = []
        return result

    amounts = result["amount"].astype(float)
    mean = float(amounts.mean())
    std = float(amounts.std(ddof=0)) or 1.0
    z = (amounts - mean) / std
    result["zscore"] = z
    result["is_outlier"] = z.abs() >= config.zscore_threshold
    return result

# trend.py

import pandas as pd
from typing import Dict
from config import (
    TREND_SHORT_MA_RATIO,
    TREND_LONG_MA_RATIO,
    TREND_NEUTRAL_THRESHOLD
)


class TrendAnalyzer:
    @staticmethod
    def analyze(df: pd.DataFrame) -> dict:
        """
        MA-based trend analysis.
        Returns trend label and strength.
        """

        prices = df["price"]

        length = len(prices)
        if length < 5:
            return {"trend": "NEUTRAL", "trend_strength": 0.0}

        short_window = max(2, int(length * TREND_SHORT_MA_RATIO))
        long_window = max(short_window + 1, int(length * TREND_LONG_MA_RATIO))

        short_ma = prices.tail(short_window).mean()
        long_ma = prices.tail(long_window).mean()

        diff_ratio = (short_ma - long_ma) / long_ma

        if abs(diff_ratio) < TREND_NEUTRAL_THRESHOLD:
            trend = "NEUTRAL"
        elif diff_ratio > 0:
            trend = "UP"
        else:
            trend = "DOWN"

        return {
            "trend": trend,
            "trend_strength": abs(diff_ratio)
        }

    def process_all(self, windowed_data: Dict[int, pd.DataFrame]) -> Dict[int, dict]:
        """
        Apply trend analysis to all windows.
        """
        results = {}

        for days, df in windowed_data.items():
            results[days] = self.analyze(df)

        return results

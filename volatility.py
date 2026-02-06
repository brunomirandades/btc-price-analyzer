# volatility.py

from typing import Dict
from config import ANNUALIZATION_FACTOR, VOLATILITY_THRESHOLDS


class VolatilityAnalyzer:
    @staticmethod
    def annualize_volatility(std_return: float) -> float:
        """
        Convert daily/hourly return std into annualized volatility.
        """
        return std_return * ANNUALIZATION_FACTOR

    @staticmethod
    def classify_volatility(annual_vol: float) -> str:
        """
        Classify volatility level based on configured thresholds.
        """
        if annual_vol < VOLATILITY_THRESHOLDS["LOW"]:
            return "LOW"
        elif annual_vol < VOLATILITY_THRESHOLDS["MEDIUM"]:
            return "MEDIUM"
        else:
            return "HIGH"

    def process_all(self, stats_by_window: Dict[int, dict]) -> Dict[int, dict]:
        """
        Adds volatility metrics for all time windows.

        Returns:
        {
            days: {
                "annual_volatility": float,
                "volatility_label": str
            }
        }
        """
        results = {}

        for days, stats in stats_by_window.items():
            annual_vol = self.annualize_volatility(stats["std_return"])
            label = self.classify_volatility(annual_vol)

            results[days] = {
                "annual_volatility": float(annual_vol),
                "volatility_label": label
            }

        return results
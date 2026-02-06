# probability_model.py

from scipy.stats import norm
from typing import Dict


class ProbabilityModel:
    @staticmethod
    def calculate_probabilities(mean_return: float, std_return: float) -> dict:
        """
        Estimate probability of next return being positive or negative.

        Uses normal distribution assumption.
        """

        # Handle edge case: no volatility
        if std_return == 0:
            return {"p_up": 0.5, "p_down": 0.5}

        # Z-score for return = 0
        z_score = (0 - mean_return) / std_return

        # CDF gives P(return <= 0)
        p_down = norm.cdf(z_score)
        p_up = 1 - p_down

        return {
            "p_up": float(p_up),
            "p_down": float(p_down)
        }

    def process_all(self, stats_by_window: Dict[int, dict]) -> Dict[int, dict]:
        """
        Apply probability model to all time windows.

        Returns:
        {
            days: {
                "p_up": float,
                "p_down": float
            }
        }
        """
        results = {}

        for days, stats in stats_by_window.items():
            probs = self.calculate_probabilities(
                stats["mean_return"],
                stats["std_return"]
            )
            results[days] = probs

        return results
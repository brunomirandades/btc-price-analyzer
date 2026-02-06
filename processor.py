# processor.py

import pandas as pd
import numpy as np
from typing import Dict


class DataProcessor:
    @staticmethod
    def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds a 'returns' column to the dataframe:
        r_t = (P_t - P_{t-1}) / P_{t-1}
        """
        df = df.copy()
        df["returns"] = df["price"].pct_change()
        df = df.dropna().reset_index(drop=True)
        return df

    @staticmethod
    def calculate_statistics(df: pd.DataFrame) -> dict:
        """
        Calculate mean and standard deviation of returns.
        Returns a dictionary:
        {
            "mean_return": float,
            "std_return": float
        }
        """
        if "returns" not in df.columns or len(df) < 2:
            return {"mean_return": 0.0, "std_return": 0.0}

        mean_return = float(np.mean(df["returns"]))
        std_return = float(np.std(df["returns"], ddof=1))  # sample std

        return {
            "mean_return": mean_return,
            "std_return": std_return
        }

    def process_windows(self, windows: Dict[int, pd.DataFrame]) -> Dict[int, dict]:
        """
        Process all time windows.
        Returns:
        {
            days: {
                "mean_return": float,
                "std_return": float,
                "open_price": float,
                "close_price": float
            }
        }
        """
        results = {}

        for days, df in windows.items():
            df_with_returns = self.compute_returns(df)
            stats = self.calculate_statistics(df_with_returns)

            open_price = float(df["price"].iloc[0])
            close_price = float(df["price"].iloc[-1])
            change_pct = (close_price - open_price) / open_price

            results[days] = {
                **stats,
                "open_price": open_price,
                "close_price": close_price,
                "change_pct": change_pct
            }

        return results
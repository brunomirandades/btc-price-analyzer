# data_fetcher.py

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict
import time

from config import VS_CURRENCY, COINGECKO_URL, COINBASE_URL

class DataFetcher:
    def __init__(self):
        self.session = requests.Session()

    # =========================
    # PRIMARY API (CoinGecko)
    # =========================
    def _fetch_from_coingecko(self, days: int) -> pd.DataFrame:
        params = {
            "vs_currency": VS_CURRENCY,
            "days": days
        }

        response = self.session.get(
            COINGECKO_URL,
            params=params,
            timeout=10
        )

        if response.status_code == 429:
            raise RuntimeError("CoinGecko rate limit hit")

        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df.sort_values("timestamp").reset_index(drop=True)

    # =========================
    # FALLBACK API (Coinbase)
    # =========================
    def _fetch_from_coinbase(self, days: int) -> pd.DataFrame:
        # Coinbase granularity: 1h = 3600
        end = datetime.utcnow()
        start = end - timedelta(days=days)

        params = {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "granularity": 3600
        }

        response = self.session.get(
            COINBASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        # Coinbase format:
        # [ time, low, high, open, close, volume ]
        df = pd.DataFrame(
            data,
            columns=["timestamp", "low", "high", "open", "close", "volume"]
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df["price"] = df["close"]

        return df[["timestamp", "price"]].sort_values("timestamp").reset_index(drop=True)

    # =========================
    # PUBLIC FETCH METHOD
    # =========================
    def fetch_market_data(self, days: int = 30) -> pd.DataFrame:
        try:
            return self._fetch_from_coingecko(days)

        except Exception as e:
            print(f"⚠️ CoinGecko failed: {e}")
            print("➡️ Switching to Coinbase fallback...")
            time.sleep(2)
            return self._fetch_from_coinbase(days)

    def split_by_time_windows(self, df: pd.DataFrame, windows: list[int]) -> Dict[int, pd.DataFrame]:
        now = datetime.utcnow()
        result = {}

        for days in windows:
            cutoff = now - timedelta(days=days)
            window_df = df[df["timestamp"] >= cutoff].copy()

            if len(window_df) < 2:
                continue

            result[days] = window_df.reset_index(drop=True)

        return result

    def get_current_price(self, df: pd.DataFrame) -> float:
        return float(df["price"].iloc[-1])

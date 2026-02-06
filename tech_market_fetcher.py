# tech_market_fetcher.py

import csv
import io
import requests

TECH_SYMBOL = "QQQ"
STOOQ_URL = "https://stooq.com/q/d/l/?s=qqq.us&i=d"


class TechMarketFetcher:
    def get_period_changes(self, windows: list[int]) -> dict[int, float | None]:
        max_days = max(windows)
        closes = self._fetch_from_stooq(max_days)

        changes = {}
        for days in windows:
            if len(closes) >= days + 1:
                start = closes[-days - 1]
                end = closes[-1]
                changes[days] = (end - start) / start
            else:
                changes[days] = None

        return changes

    def _fetch_from_stooq(self, max_days: int) -> list[float]:
        response = requests.get(STOOQ_URL, timeout=10)
        response.raise_for_status()

        reader = csv.DictReader(io.StringIO(response.text))
        closes = [
            float(row["Close"])
            for row in reader
            if row["Close"] != "-"
        ]

        # Ensure enough data
        return closes[-(max_days + 1):]

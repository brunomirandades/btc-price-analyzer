# main.py

import time
import sys

from config import TIME_WINDOWS, REFRESH_INTERVAL_SECONDS
from data_fetcher import DataFetcher
from processor import DataProcessor
from probability_model import ProbabilityModel
from volatility import VolatilityAnalyzer
from trend import TrendAnalyzer
from display import Display


def run():
    fetcher = DataFetcher()
    processor = DataProcessor()
    prob_model = ProbabilityModel()
    volatility = VolatilityAnalyzer()
    trend_analyzer = TrendAnalyzer()
    display = Display()
    display.hide_cursor()

    try:
        while True:
            try:
                # Getting API info message
                display.renderLoadingInfo()
                
                # 1. Fetch market data
                max_days = max(TIME_WINDOWS)
                full_df = fetcher.fetch_market_data(days=max_days)

                # 2. Split windows
                windowed_data = fetcher.split_by_time_windows(
                    full_df,
                    TIME_WINDOWS
                )

                # 3. Current price
                current_price = fetcher.get_current_price(full_df)

                # 4. Stats
                stats_by_window = processor.process_windows(windowed_data)

                # 5. Probability
                probabilities = prob_model.process_all(stats_by_window)

                # 6. Volatility
                volatility_data = volatility.process_all(stats_by_window)

                # 7. Trend
                trend_data = trend_analyzer.process_all(windowed_data)

                # 8. Merge all analytics
                merged_data = {}
                for days in stats_by_window.keys():
                    merged_data[days] = {
                        **stats_by_window[days],
                        **probabilities.get(days, {}),
                        **volatility_data.get(days, {}),
                        **trend_data.get(days, {})
                    }

                # 9. Render
                display.render(
                    current_price=current_price,
                    window_data=merged_data
                )

                # 10. Sleep
                time.sleep(REFRESH_INTERVAL_SECONDS)

            except Exception as e:
                display.show_cursor()
                display.clear()
                print("⚠️ Temporary error occurred. Retrying in 30 seconds...")
                print(str(e))
                time.sleep(30)
                display.hide_cursor()


    except KeyboardInterrupt:
        display.show_cursor()
        display.clear()
        print("👋 BTC Market Analyzer stopped. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    run()

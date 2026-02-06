# config.py

from math import sqrt

# -------------------------
# API ENDPOINTS
# -------------------------
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
COINBASE_URL = "https://api.exchange.coinbase.com/products/BTC-USD/candles"

# =========================
# API CONFIGURATION
# =========================
VS_CURRENCY = "usd"

# =========================
# TIME WINDOWS (IN DAYS)
# =========================
TIME_WINDOWS = [30, 15, 10, 5, 3, 1]

# =========================
# REFRESH SETTINGS
# =========================
REFRESH_INTERVAL_SECONDS = 600  # 10 minutes

# =========================
# VOLATILITY SETTINGS
# =========================
ANNUALIZATION_FACTOR = sqrt(365)

VOLATILITY_THRESHOLDS = {
    "LOW": 0.40,
    "MEDIUM": 0.80
    # HIGH = anything above MEDIUM
}

# =========================
# TREND / MOMENTUM SETTINGS
# =========================
TREND_SHORT_MA_RATIO = 0.2   # 20% of window
TREND_LONG_MA_RATIO = 0.5    # 50% of window
TREND_NEUTRAL_THRESHOLD = 0.002  # 0.2% difference

# =========================
# DISPLAY SETTINGS
# =========================
APP_TITLE = "BITCOIN MARKET ANALYZER"

# =========================
# S&P500 IT Market info
# =========================
TECH_SYMBOL = "QQQ"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}"
STOOQ_URL = "https://stooq.com/q/d/l/?s=qqq.us&i=d"
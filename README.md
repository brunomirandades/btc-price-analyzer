# Bitcoin Market Analyzer

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Terminal](https://img.shields.io/badge/interface-terminal-black)
![Status](https://img.shields.io/badge/status-experimental-orange)

A lightweight terminal-based Bitcoin market analysis tool written in Python.

The application periodically fetches Bitcoin price data, analyzes multiple historical time windows, and displays trend direction, volatility, heuristic probabilities, and a comparison against the S&P 500 Technology sector directly in your terminal.

⚠️ This project is for educational and analytical purposes only.  
It is **not financial advice**.

---

## Features

- Fetches real Bitcoin market data (CoinGecko)
- Analyzes multiple rolling time windows:
  - 30d, 15d, 10d, 5d, 3d, 1d
- Displays per period:
  - BTC period price change (%)
  - BTC trend (UP / DOWN / NEUTRAL)
  - Probability of price moving UP or DOWN (heuristic)
  - Market volatility (LOW / MEDIUM / HIGH)
  - S&P 500 Technology sector change (%) (proxy via QQQ)
- Auto-refresh every 10 minutes
- Terminal-friendly UI with colors (Rich)
- Graceful exit (no tracebacks)
- Cursor hidden while running
- Brazil-local timestamps (UTC-3)

---

## Preview (example)

```text
BITCOIN MARKET ANALYZER
Current Price: $63,573.03    Last Update: 20:42:41 (UTC-3)

Period | BTC Δ    | Tech Δ | Trend | P(UP) | P(DOWN) | Volatility
----------------------------------------------------------------
30d    | -32.11%  | +4.12% | DOWN  | 46%   | 54%     | LOW
15d    | -28.89%  | +3.01% | DOWN  | 44%   | 56%     | LOW
10d    | -27.94%  | +2.44% | DOWN  | 43%   | 57%     | LOW
5d     | -19.16%  | +1.88% | DOWN  | 42%   | 58%     | LOW
3d     | -19.18%  | -0.32% | DOWN  | 39%   | 61%     | LOW
1d     | -12.94%  | -0.91% | DOWN  | 30%   | 70%     | LOW
```

---

## Data Sources

- **Bitcoin market data**: CoinGecko (free tier, rate-limit safe)
- **Tech market proxy**: Stooq (QQQ daily data, no API key required)

---

## Requirements

- Python 3.10+
- Linux / macOS / Windows (WSL supported)

### Python dependencies

- requests
- pandas
- numpy
- scipy
- rich

All dependencies are listed in `requirements.txt`.

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd btc-price-analyzer
```

---

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

If needed on Ubuntu/Debian:

```bash
sudo apt install python3-venv python3-full
```

---

### 3. Activate the virtual environment

```bash
source .venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Recommended (via script)

```bash
chmod +x run.sh
./run.sh
```

---

### Manual run

```bash
source .venv/bin/activate
python main.py
```

---

## Optional: Shell Alias

To run the app from anywhere, add this to `~/.bashrc`:

```bash
alias btctrend="cd <your dir here>/btc-price-analyzer && ./run.sh"
```

Reload:

```bash
source ~/.bashrc
```

Then run:

```bash
btctrend
```

---

## Project Structure

```text
btc-price-analyzer/
├── main.py
├── config.py
├── data_fetcher.py
├── processor.py
├── probability_model.py
├── volatility.py
├── trend.py
├── tech_market_fetcher.py
├── display.py
├── requirements.txt
├── run.sh
├── .gitignore
└── README.md
```

---

## Notes

- Probabilities are heuristic, not predictive
- BTC trades 24/7; equities trade on weekdays only
- Short-term divergence between BTC and tech markets is expected
- No API keys are required

---

## Disclaimer

This tool does not provide financial advice.  
Use it responsibly and at your own risk.

---

## License

MIT

#!/usr/bin/env bash

# Stop on first error
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
  echo "❌ Virtual environment not found."
  echo "👉 Create it first with:"
  echo "   python3 -m venv .venv"
  exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Install dependencies
echo "🔧 Checking dependencies..."
pip install -r requirements.txt

# Run the application
echo "🚀 Starting Bitcoin Market Analyzer..."
python main.py

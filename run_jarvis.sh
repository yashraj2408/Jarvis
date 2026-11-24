#!/usr/bin/env bash
# J.A.R.V.I.S. Launcher for macOS and Linux
set -e

echo "====================================================================="
echo "          ⚡ J.A.R.V.I.S. - STARK INDUSTRIES OS LAUNCHER ⚡"
echo "====================================================================="
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "[INFO] Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

echo "[INFO] Activating virtual environment..."
source .venv/bin/activate

echo "[INFO] Installing / verifying required libraries..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "====================================================================="
echo "[SUCCESS] J.A.R.V.I.S. is ready! Launching web interface..."
echo "====================================================================="
echo ""

python3 -m streamlit run streamlit_app.py

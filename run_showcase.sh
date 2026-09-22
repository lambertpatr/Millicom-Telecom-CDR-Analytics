#!/usr/bin/env bash
# =============================================================================
# Run Streamlit Enterprise Client Showcase Portal
# =============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${PORT:-8501}"
HOST="${HOST:-0.0.0.0}"

echo "================================================================="
echo "⚡ Launching Enterprise Data Science Client Showcase Portal"
echo "📂 Working Directory: $SCRIPT_DIR"
echo "🌐 Binding: http://$HOST:$PORT"
echo "================================================================="

# Activate virtual environment if present
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    echo "Using local venv..."
    source "$SCRIPT_DIR/venv/bin/activate"
elif [ -f "/home/lambert/Desktop/fast-api/.venv/bin/activate" ]; then
    echo "Using VPS fast-api .venv..."
    source "/home/lambert/Desktop/fast-api/.venv/bin/activate"
elif [ -f "$HOME/.venv/bin/activate" ]; then
    source "$HOME/.venv/bin/activate"
fi

python3 -m streamlit run streamlit_app.py \
    --server.port="$PORT" \
    --server.address="$HOST" \
    --server.headless=true \
    --browser.gatherUsageStats=false \
    --theme.base="light" \
    --theme.primaryColor="#0284C7"

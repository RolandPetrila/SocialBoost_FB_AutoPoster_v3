#!/bin/bash
set -euo pipefail

echo "🚀 Starting SocialBoost v3 Web GUI..."
export PYTHONUNBUFFERED=1
# Streamlit picks up .env automatically for env vars
streamlit run GUI_Web/app.py --server.port 8501 --server.address 0.0.0.0

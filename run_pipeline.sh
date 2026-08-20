#!/bin/bash
set -e

VENV_PYTHON="venv/bin/python"

echo "=== 1. Running Data Ingestion ==="
$VENV_PYTHON ingest.py

echo "=== 2. Running Data Transformation ==="
$VENV_PYTHON transform.py

echo "=== 3. Running Analytics & Visualization ==="
$VENV_PYTHON analytics.py

echo "=== 4. Building Feature Store (SQLite) ==="
$VENV_PYTHON feature_store.py

echo "=== 5. Training Churn Prediction Model ==="
$VENV_PYTHON train.py

echo "=========================================="
echo "Pipeline execution finished successfully!"
echo "To start Model Serving API: venv/bin/uvicorn serve:app --reload --port 8000"
echo "To start Streamlit UI: venv/bin/streamlit run streamlit_app.py"
echo "=========================================="

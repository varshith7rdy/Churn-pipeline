#!/bin/bash
set -e

# Use virtual environment python if present, fallback to system python3
VENV_PYTHON="venv/bin/python"
if [ ! -f "$VENV_PYTHON" ]; then
    VENV_PYTHON="python3"
fi

# Auto-download dataset if missing
if [ ! -f "data/raw/telco_churn.csv" ] && [ ! -f "WA_Fn-UseC_-Telco-Customer-Churn.csv" ]; then
    echo "Dataset missing. Downloading Telco Customer Churn dataset..."
    curl -L -o WA_Fn-UseC_-Telco-Customer-Churn.csv "https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    mkdir -p data/raw
    cp WA_Fn-UseC_-Telco-Customer-Churn.csv data/raw/telco_churn.csv
elif [ ! -f "data/raw/telco_churn.csv" ] && [ -f "WA_Fn-UseC_-Telco-Customer-Churn.csv" ]; then
    mkdir -p data/raw
    cp WA_Fn-UseC_-Telco-Customer-Churn.csv data/raw/telco_churn.csv
fi

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

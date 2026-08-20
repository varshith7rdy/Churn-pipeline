# Telecom Customer Churn ML Pipeline

An end-to-end Machine Learning data pipeline for telecom customer churn prediction covering extraction, ingestion, transformation, analytics, SQLite feature store, model training, model serving API, reverse ETL prediction logging, and a Streamlit UI.

## Quick Start

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run Core Pipeline (Ingest → Transform → Analytics → Feature Store → Train)**:
   ```bash
   bash run_pipeline.sh
   ```

3. **Start Model Serving API**:
   ```bash
   venv/bin/uvicorn serve:app --reload --port 8000
   ```

4. **Start Streamlit Inference UI**:
   ```bash
   STREAMLIT_CONFIG_DIR=.streamlit venv/bin/streamlit run streamlit_app.py
   ```

## Detailed Operating Instructions

For step-by-step guidance on running individual components, uploading datasets, querying the SQLite Feature Store, and inspecting prediction logs, refer to the complete [OPERATING_GUIDE.md](file:///home/varshith/churn-l5/OPERATING_GUIDE.md).

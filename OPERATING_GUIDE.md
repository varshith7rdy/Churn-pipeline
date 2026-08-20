# Telecom Customer Churn ML Pipeline — Operating Guide

This guide provides step-by-step instructions on how to operate, run, test, and manage the end-to-end Machine Learning Data Pipeline.

---

## Table of Contents
1. [Prerequisites & Virtual Environment Setup](#1-prerequisites--virtual-environment-setup)
2. [Project Architecture & File Layout](#2-project-architecture--file-layout)
3. [Running the Automated Pipeline (All-in-One)](#3-running-the-automated-pipeline-all-in-one)
4. [Running Pipeline Components Manually (Step-by-Step)](#4-running-pipeline-components-manually-step-by-step)
   - [Step 0: Data Extraction API](#step-0-data-extraction-api)
   - [Step 1: Data Ingestion](#step-1-data-ingestion)
   - [Step 2: Data Transformation](#step-2-data-transformation)
   - [Step 3: Data Analytics](#step-3-data-analytics)
   - [Step 4: SQLite Feature Store](#step-4-sqlite-feature-store)
   - [Step 5: Model Training](#step-5-model-training)
   - [Step 6 & 7: Model Serving API & Reverse ETL](#step-6--7-model-serving-api--reverse-etl)
   - [Step 8: Streamlit Inference UI](#step-8-streamlit-inference-ui)
5. [Monitoring & Inspected Data Artifacts](#5-monitoring--inspected-data-artifacts)
6. [Troubleshooting & FAQs](#6-troubleshooting--faqs)

---

## 1. Prerequisites & Virtual Environment Setup

The pipeline runs inside an isolated Python virtual environment located at `venv/`.

### Activate Virtual Environment
```bash
source venv/bin/activate
```

*(If you ever need to re-create the virtual environment from scratch:)*
```bash
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install fastapi uvicorn pandas scikit-learn matplotlib seaborn joblib streamlit requests
```

---

## 2. Project Architecture & File Layout

```
churn-l5/
├── venv/                       # Python Virtual Environment
├── data/
│   ├── raw/                    # Raw uploaded dataset (telco_churn.csv)
│   ├── processed/              # Cleaned & feature-engineered dataset (telco_processed.csv)
│   ├── analytics/              # CSV summaries and visualization charts (.png)
│   └── prediction_logs/        # Reverse ETL inference logs (predictions.csv)
├── raw_zone/                   # Ingestion staging directory
├── model_store/
│   ├── feature_store.db        # SQLite Feature Store database
│   └── churn_model.pkl         # Trained Random Forest model binary
├── .streamlit/
│   └── config.toml             # Headless configuration for Streamlit UI
├── extract_api_server.py       # FastAPI Data Extraction Upload Endpoint (Port 9000)
├── ingest.py                   # Ingestion module (Raw -> Raw Zone)
├── transform.py                # Data Cleaning & Feature Engineering
├── analytics.py                # Business Analytics & Visualization
├── feature_store.py            # SQLite Feature Store Builder
├── train.py                    # Model Trainer & Evaluator
├── serve.py                    # FastAPI Prediction Scoring API (Port 8000)
├── reverse_etl.py              # Prediction Logging Module
├── streamlit_app.py            # Streamlit Interactive Inference UI (Port 8501)
├── run_pipeline.sh             # Master Pipeline Automation Script
└── OPERATING_GUIDE.md          # Operating Instructions
```

---

## 3. Running the Automated Pipeline (All-in-One)

To execute the core ETL, Analytics, Feature Store, and Model Training steps sequentially in one command:

```bash
bash run_pipeline.sh
```

**What this script does:**
1. Runs `ingest.py` (copies `data/raw/*.csv` to `raw_zone/`).
2. Runs `transform.py` (cleans nulls, calculates `tenure_group`, `avg_monthly_charges`, `churn_flag`).
3. Runs `analytics.py` (exports statistical summaries and `churn_by_contract.png`).
4. Runs `feature_store.py` (builds `model_store/feature_store.db`).
5. Runs `train.py` (trains Random Forest classifier, evaluates Accuracy & ROC-AUC, saves `model_store/churn_model.pkl`).

---

## 4. Running Pipeline Components Manually (Step-by-Step)

### Step 0: Data Extraction API (Upload Endpoint)
Start the Data Extraction API on port `9000`:
```bash
venv/bin/uvicorn extract_api_server:app --reload --port 9000
```
In another terminal, upload a raw CSV dataset to the API:
```bash
curl -X POST "http://127.0.0.1:9000/upload-dataset" -F "file=@WA_Fn-UseC_-Telco-Customer-Churn.csv"
```
*Output file:* `data/raw/telco_churn.csv`

---

### Step 1: Data Ingestion
Copy extracted dataset into the staged `raw_zone`:
```bash
venv/bin/python ingest.py
```
*Output file:* `raw_zone/telco_churn.csv`

---

### Step 2: Data Transformation
Clean numeric columns, handle missing charges, and construct derived feature columns:
```bash
venv/bin/python transform.py
```
*Output file:* `data/processed/telco_processed.csv`

---

### Step 3: Data Analytics
Generate summary CSV statistics, contract churn rates, feature correlation metrics, and PNG plots:
```bash
venv/bin/python analytics.py
```
*Output directory:* `data/analytics/`

---

### Step 4: SQLite Feature Store Creation
Construct one-hot encoded feature matrix and persist to SQLite database:
```bash
venv/bin/python feature_store.py
```
*Output file:* `model_store/feature_store.db` (Table: `features`)

---

### Step 5: Model Training
Train a Random Forest Classifier (`n_estimators=200`) on 80/20 train/test split:
```bash
venv/bin/python train.py
```
*Output model:* `model_store/churn_model.pkl`

---

### Step 6 & 7: Model Serving API & Reverse ETL
Launch the FastAPI scoring server on port `8000`:
```bash
venv/bin/uvicorn serve:app --reload --port 8000
```

#### Test Prediction Endpoint (`POST /predict`)
Send a sample customer feature payload to score churn probability:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "features": {
         "SeniorCitizen": 0,
         "MonthlyCharges": 70.35,
         "TotalCharges": 1397.47,
         "tenure": 20,
         "avg_monthly_charges": 69.87,
         "gender_Male": 1,
         "Partner_Yes": 0,
         "Dependents_Yes": 0,
         "PhoneService_Yes": 1,
         "InternetService_Fiber optic": 1,
         "Contract_One year": 0,
         "Contract_Two year": 0,
         "PaymentMethod_Electronic check": 1
       }
     }'
```
*Expected Response:* `{"churn_probability": 0.305}`

#### Reverse ETL Log File
Each prediction request automatically appends timestamped features and predicted probabilities to:
`data/prediction_logs/predictions.csv`

---

### Step 8: Streamlit Inference UI
Launch the interactive web user interface on port `8501`:
```bash
STREAMLIT_CONFIG_DIR=.streamlit venv/bin/streamlit run streamlit_app.py
```
Access the application in your browser at:
`http://localhost:8501`

---

## 5. Monitoring & Inspected Data Artifacts

You can inspect the contents of any generated artifact using standard shell commands or Python:

- **Check Processed Data Row Count**:
  ```bash
  wc -l data/processed/telco_processed.csv
  ```

- **Inspect Feature Store Tables (SQLite)**:
  ```bash
  sqlite3 model_store/feature_store.db ".schema features"
  ```

- **View Recent Prediction Logs**:
  ```bash
  tail -n 10 data/prediction_logs/predictions.csv
  ```

---

## 6. Troubleshooting & FAQs

- **Port in use error (`Address already in use`)**:
  Kill any lingering process on ports 9000, 8000, or 8501:
  ```bash
  fuser -k 9000/tcp 8000/tcp 8501/tcp
  ```

- **ModuleNotFoundError**:
  Ensure you are executing scripts using `venv/bin/python` or after running `source venv/bin/activate`.

- **Streamlit Prompting for Email on Startup**:
  Ensure `.streamlit/config.toml` exists with `[browser] gatherUsageStats = false` or run with `STREAMLIT_CONFIG_DIR=.streamlit`.

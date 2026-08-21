# 📡 Telecom Customer Churn ML Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Feature%20Store-003B57.svg)](https://www.sqlite.org/)

An end-to-end Machine Learning data pipeline built for **Telecom Customer Churn Prediction**. It demonstrates modern DataOps & MLOps practices across the full lifecycle:

```
[Raw CSV Dataset] 
       │
       ▼
 [Step 0: FastAPI Extraction API] ──► Uploads raw data to data/raw/
       │
       ▼
 [Step 1: Ingestion Module]       ──► Stages data into raw_zone/
       │
       ▼
 [Step 2: Transformation Engine]  ──► Cleans nulls & engineers features -> data/processed/
       │
       ▼
 [Step 3: Analytics Engine]       ──► Exports metrics & visual charts -> data/analytics/
       │
       ▼
 [Step 4: SQLite Feature Store]   ──► Stores one-hot encoded features -> model_store/feature_store.db
       │
       ▼
 [Step 5: Random Forest Trainer]  ──► Trains classifier & saves model -> model_store/churn_model.pkl
       │
       ├───────────────────────────────┐
       ▼                               ▼
 [Step 7: Serving API (FastAPI)] ◄──► [Step 8: Streamlit Inference UI]
       │
       ▼
 [Step 6: Reverse ETL]            ──► Logs predictions to data/prediction_logs/predictions.csv
```

---

## 📋 Prerequisites

Before setting up the project, ensure you have installed:
- **Python 3.10+** (`python3 --version`)
- **pip** (`python3 -m pip --version`)
- **git** (`git --version`)
- **curl** (for API testing)

---

## 🚀 Step-by-Step Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/varshith7rdy/Churn-pipeline.git
cd Churn-pipeline
```

### 2. Create and Activate a Python Virtual Environment
It is recommended to run the pipeline inside an isolated virtual environment (`venv`).

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (Command Prompt / PowerShell):**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📊 Step 4. Download / Obtain Dataset

The pipeline requires the **Telco Customer Churn** dataset (`WA_Fn-UseC_-Telco-Customer-Churn.csv`).

Optionally download it directly using Python or `curl`:
```bash
curl -L -o WA_Fn-UseC_-Telco-Customer-Churn.csv "https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"
```

---

## ⚡ Step 5. Run the Complete Pipeline

You can run all backend stages (Ingestion → Transformation → Analytics → Feature Store → Model Training) automatically:

```bash
bash run_pipeline.sh
```

### Expected Output Summary:
- **Ingestion**: Raw file staged in `raw_zone/telco_churn.csv`.
- **Transformation**: Processed CSV created at `data/processed/telco_processed.csv`.
- **Analytics**: Business statistics & charts exported to `data/analytics/`.
- **Feature Store**: SQLite database populated at `model_store/feature_store.db`.
- **Model Training**: Random Forest model trained (`Accuracy: ~78.6%`, `ROC-AUC: ~0.692`), saved to `model_store/churn_model.pkl`.

---

## 🌐 Step 6. Model Serving API & Streamlit UI

### A. Launch the FastAPI Model Serving API
```bash
uvicorn serve:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Endpoint: `POST http://localhost:8000/predict`

#### Test Scoring via `curl`:
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
*Response:* `{"churn_probability": 0.305}`  
*Reverse ETL Logged:* Saved to `data/prediction_logs/predictions.csv`.

---

### B. Launch the Interactive Streamlit UI
In a separate terminal (with `venv` activated):
```bash
streamlit run streamlit_app.py
```
Open your browser at `http://localhost:8501` to test real-time churn prediction!

---

## 📁 Repository Directory Structure

```
Churn-pipeline/
├── .streamlit/               # Streamlit configuration settings
├── data/
│   ├── raw/                  # Extracted dataset storage
│   ├── processed/            # Feature-engineered dataset
│   ├── analytics/            # Analytics reports & plots
│   └── prediction_logs/      # Reverse ETL prediction logs
├── raw_zone/                 # Ingestion staging area
├── model_store/              # SQLite feature store & trained .pkl model
├── extract_api_server.py     # Extraction API (Upload endpoint on port 9000)
├── ingest.py                 # Data Ingestion script
├── transform.py              # Data Cleaning & Feature Engineering
├── analytics.py              # Exploratory Data Analytics
├── feature_store.py          # SQLite Feature Store builder
├── train.py                  # Random Forest training script
├── serve.py                  # FastAPI Model Serving endpoint (port 8000)
├── reverse_etl.py            # Prediction logging module
├── streamlit_app.py          # Streamlit user interface (port 8501)
├── run_pipeline.sh           # Master pipeline runner script
├── requirements.txt          # Python dependency specifications
├── OPERATING_GUIDE.md        # Comprehensive operating manual
└── README.md                 # Project Overview & Setup Guide
```

---

## 🛠️ Troubleshooting

- **`ModuleNotFoundError: No module named 'fastapi'`**:
  Make sure you activated your virtual environment (`source venv/bin/activate`) before running scripts.
- **`Port already in use` error**:
  If ports 8000, 8501, or 9000 are occupied, free them using:
  `fuser -k 8000/tcp 8501/tcp 9000/tcp`
- **Streamlit prompt for email on startup**:
  Run Streamlit with `STREAMLIT_CONFIG_DIR=.streamlit streamlit run streamlit_app.py`.

---

## 📄 License & Documentation
For full details on individual module functions and operational commands, read the [OPERATING_GUIDE.md](OPERATING_GUIDE.md).

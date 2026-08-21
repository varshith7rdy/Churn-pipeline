import streamlit as st
import requests
import pandas as pd
import sqlite3

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Telecom Customer Churn Predictor",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Telecom Customer Churn Predictor")
st.markdown("Enter customer details below with specified measurement units to evaluate real-time churn risk.")

# Feature metadata defining human-readable labels, units, tooltips, and default values
FEATURE_METADATA = {
    "tenure": {
        "label": "Tenure",
        "unit": "Months (0 to 72)",
        "help": "Total months customer has been subscribed",
        "default": 12.0, "min": 0.0, "max": 100.0, "step": 1.0
    },
    "MonthlyCharges": {
        "label": "Monthly Charges",
        "unit": "USD ($ / month)",
        "help": "Current recurring monthly charge amount",
        "default": 65.0, "min": 0.0, "max": 200.0, "step": 1.0
    },
    "TotalCharges": {
        "label": "Total Cumulative Charges",
        "unit": "USD ($ lifetime)",
        "help": "Total billing amount over entire tenure",
        "default": 780.0, "min": 0.0, "max": 10000.0, "step": 10.0
    },
    "avg_monthly_charges": {
        "label": "Average Monthly Charges",
        "unit": "USD ($ / month avg)",
        "help": "Calculated average charge per month",
        "default": 65.0, "min": 0.0, "max": 200.0, "step": 1.0
    },
    "SeniorCitizen": {
        "label": "Senior Citizen Status",
        "unit": "Binary Flag (0 = No, 1 = Yes)",
        "help": "Is customer a senior citizen (65+ years)?",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "gender_Male": {
        "label": "Gender: Male",
        "unit": "Binary Flag (1 = Male, 0 = Female)",
        "help": "Gender identity flag",
        "default": 1.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "Partner_Yes": {
        "label": "Has Partner",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Does the customer have a partner?",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "Dependents_Yes": {
        "label": "Has Dependents",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Does the customer have dependent family members?",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "PhoneService_Yes": {
        "label": "Phone Service",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Is customer subscribed to home phone service?",
        "default": 1.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "InternetService_Fiber optic": {
        "label": "Internet: Fiber Optic",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Subscribed to Fiber Optic high-speed internet",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "InternetService_No": {
        "label": "Internet: No Service",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Customer has no internet service plan",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "Contract_One year": {
        "label": "Contract: 1-Year Commitment",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "On a 1-Year subscription contract",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "Contract_Two year": {
        "label": "Contract: 2-Year Commitment",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "On a 2-Year subscription contract",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "PaymentMethod_Credit card (automatic)": {
        "label": "Payment: Credit Card (Auto)",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Automatic recurring credit card payments",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "PaymentMethod_Electronic check": {
        "label": "Payment: Electronic Check",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Settles bills via electronic check",
        "default": 1.0, "min": 0.0, "max": 1.0, "step": 1.0
    },
    "PaymentMethod_Mailed check": {
        "label": "Payment: Mailed Check",
        "unit": "Binary Flag (1 = Yes, 0 = No)",
        "help": "Settles bills via physical mailed check",
        "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0
    }
}

# Fetch canonical schema from SQLite database
conn = sqlite3.connect("model_store/feature_store.db")
db_df = pd.read_sql("SELECT * FROM features LIMIT 1", conn)
conn.close()
feature_cols = list(db_df.drop(columns=['churn_flag']).columns)

user_inputs = {}

col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Account & Billing Metrics")
    for key in ["tenure", "MonthlyCharges", "TotalCharges", "avg_monthly_charges"]:
        if key in feature_cols:
            meta = FEATURE_METADATA.get(key, {"label": key, "unit": "Numeric", "help": "", "default": 0.0, "min": 0.0, "max": 10000.0, "step": 1.0})
            field_name = f"{meta['label']}  [{meta['unit']}]"
            user_inputs[key] = st.number_input(
                field_name,
                value=meta['default'],
                min_value=meta['min'],
                max_value=meta['max'],
                step=meta['step'],
                help=meta['help']
            )

    st.subheader("👤 Customer Demographics")
    for key in ["SeniorCitizen", "gender_Male", "Partner_Yes", "Dependents_Yes"]:
        if key in feature_cols:
            meta = FEATURE_METADATA.get(key, {"label": key, "unit": "Binary 0/1", "help": "", "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0})
            field_name = f"{meta['label']}  [{meta['unit']}]"
            user_inputs[key] = st.number_input(
                field_name,
                value=meta['default'],
                min_value=meta['min'],
                max_value=meta['max'],
                step=meta['step'],
                help=meta['help']
            )

with col2:
    st.subheader("🌐 Services & Contract Commitments")
    for key in ["PhoneService_Yes", "InternetService_Fiber optic", "InternetService_No", "Contract_One year", "Contract_Two year"]:
        if key in feature_cols:
            meta = FEATURE_METADATA.get(key, {"label": key, "unit": "Binary 0/1", "help": "", "default": 0.0, "min": 0.0, "max": 10000.0, "step": 1.0})
            field_name = f"{meta['label']}  [{meta['unit']}]"
            user_inputs[key] = st.number_input(
                field_name,
                value=meta['default'],
                min_value=meta['min'],
                max_value=meta['max'],
                step=meta['step'],
                help=meta['help']
            )

    st.subheader("🏦 Payment Method Options")
    for key in ["PaymentMethod_Credit card (automatic)", "PaymentMethod_Electronic check", "PaymentMethod_Mailed check"]:
        if key in feature_cols:
            meta = FEATURE_METADATA.get(key, {"label": key, "unit": "Binary 0/1", "help": "", "default": 0.0, "min": 0.0, "max": 1.0, "step": 1.0})
            field_name = f"{meta['label']}  [{meta['unit']}]"
            user_inputs[key] = st.number_input(
                field_name,
                value=meta['default'],
                min_value=meta['min'],
                max_value=meta['max'],
                step=meta['step'],
                help=meta['help']
            )

# Fill any remaining unspecified schema columns
for col in feature_cols:
    if col not in user_inputs:
        user_inputs[col] = 0.0

st.divider()

if st.button("📊 Evaluate Churn Probability", type="primary", use_container_width=True):
    payload = {"features": user_inputs}
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            prob = response.json()['churn_probability']
            pct = prob * 100

            st.subheader("Inference Result")
            if prob >= 0.60:
                st.error(f"⚠️ **HIGH RISK OF CHURN**: Estimated Probability = **{prob:.2f} ({pct:.1f}%)**")
            elif prob >= 0.30:
                st.warning(f"⚡ **MODERATE RISK OF CHURN**: Estimated Probability = **{prob:.2f} ({pct:.1f}%)**")
            else:
                st.success(f"✅ **LOW RISK OF CHURN (RETENTION STABLE)**: Estimated Probability = **{prob:.2f} ({pct:.1f}%)**")
        else:
            st.error(f"API Error ({response.status_code}): Could not score churn risk. Check FastAPI server logs.")
    except Exception as e:
        st.error(f"Connection Error: Unable to reach FastAPI backend at `{API_URL}`. Ensure `serve.py` is running.")
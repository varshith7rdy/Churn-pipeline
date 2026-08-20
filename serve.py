from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import sqlite3
from reverse_etl import log_prediction

app = FastAPI()
model = joblib.load("model_store/churn_model.pkl")

conn = sqlite3.connect("model_store/feature_store.db")
prototype = pd.read_sql("SELECT * FROM features LIMIT 1", conn)
conn.close()
feature_cols = list(prototype.drop(columns=['churn_flag']).columns)

class CustomerFeatures(BaseModel):
    features: dict

@app.post("/predict")
def predict(data: CustomerFeatures):
    x = np.array([data.features.get(col, 0) for col in feature_cols]).reshape(1, -1)
    prob = float(model.predict_proba(x)[0][1])
    log_prediction(data.features, prob)
    return {"churn_probability": prob}
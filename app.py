from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from datetime import datetime
from typing import List
import httpx


app = FastAPI(debug= True )

class CDFInput(BaseModel):
    InvoiceNo: List[int]
    StockCode: List[str]
    Description: List[str]
    Quantity: List[int]
    InvoiceDate: List[str]
    UnitPrice: List[int]
    CustomerID: List[int]
    Country: List[str]

class RFMInput(BaseModel):
    Recency: int
    Frequency: int
    Revenue: int

# Load the pre-trained RF model
model = joblib.load(r"C:/Users/vedant raikar/Desktop/sql query nlp interface/rf_model.joblib")
# Specify the path to your JSON file


@app.get("/main")
async def main():
    return{"HI"}

@app.post("/predict")
async def predict(cdf: CDFInput):
    try:
        rfm_data = await calc_rfm(cdf)
        df = pd.DataFrame(rfm_data)
        clv_predictions = model.predict(df)
        return {"clv_predictions": clv_predictions.tolist()}
    except Exception as e:
        return {"error": str(e)}

async def calc_rfm(cdf: CDFInput):
    try:
        df = pd.DataFrame(cdf.dict())
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        current_date = max(df['InvoiceDate'])
        recency_df = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
        recency_df['Recency'] = (current_date - recency_df['InvoiceDate']).dt.days
        recency_df.drop('InvoiceDate', axis=1, inplace=True)
        frequency_df = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
        frequency_df.columns = ['CustomerID', 'Frequency']
        monetary_df = df.groupby('CustomerID')['Quantity'].sum().reset_index()
        monetary_df.columns = ['CustomerID', 'Revenue']
        rfm_df = recency_df.merge(frequency_df, on='CustomerID').merge(monetary_df, on='CustomerID')
        rfm_df = rfm_df.drop('CustomerID', axis=1)
        return rfm_df.to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}

@app.post("/calculate")
async def calc_rfm(cdf: CDFInput):
    try:
        df = pd.DataFrame(cdf.dict())
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        current_date = max(df['InvoiceDate'])
        recency_df = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
        recency_df['Recency'] = (current_date - recency_df['InvoiceDate']).dt.days
        recency_df.drop('InvoiceDate', axis=1, inplace=True)
        frequency_df = df.groupby('CustomerID')['InvoiceNo'].count().reset_index()
        frequency_df.columns = ['CustomerID', 'Frequency']
        monetary_df = df.groupby('CustomerID')['Quantity'].sum().reset_index()
        monetary_df.columns = ['CustomerID', 'Revenue']
        rfm_df = recency_df.merge(frequency_df, on='CustomerID').merge(monetary_df, on='CustomerID')
        rfm_df = rfm_df.drop('CustomerID' , axis= 1)
        return rfm_df.to_dict(orient='records')
    except Exception as e:
        return {"error": str(e)}




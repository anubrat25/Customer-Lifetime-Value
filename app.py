from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

class cdf(BaseModel):
     InvoiceNo: int
     StockCode: str 
     Description: str 
     Quantity: int 
     InvoiceDate: str 
     UnitPrice: int 
     CustomerID: int 
     Country: str 


     
class RFMInput(BaseModel):
    Recency: int
    Frequency: int
    Revenue: int

# Define the prediction endpoint
@app.post("/")
async def main ():
    return {'welcome to clv prediction api'}



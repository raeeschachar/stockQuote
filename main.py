from datetime import datetime

from fastapi import FastAPI
import requests
from pydantic import BaseModel

import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class DataPriceBase(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    price: float
    volume: int
    latest_trading_day: datetime
    previous_close: float
    change: float
    change_percentage: float

    class Config:
        from_attributes = True


db = SessionLocal()


@app.get("/stock/quote")
def root():
    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function": "GLOBAL_QUOTE", "symbol": "MSFT", "datatype": "json"}

    headers = {
        "X-RapidAPI-Key": "ADD-KEY",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    quote_response = response.json()

    # Add data to DB
    db_quote_data = models.PriceData(symbol=quote_response.get("01. symbol"),
                                     open=quote_response.get("02. open"),
                                     high=quote_response.get("03. high"),
                                     low=quote_response.get("04. low"),
                                     price=quote_response.get("05. price"),
                                     volume=quote_response.get("06. volume"),
                                     latest_trading_day=quote_response.get("07. latest trading day"),
                                     previous_close=quote_response.get("08. previous close"),
                                     change=quote_response.get("09. change"),
                                     change_percentage=quote_response.get("10. change percent")
                                     )
    db.add(db_quote_data)
    db.commit()
    print(db_quote_data)

    return quote_response

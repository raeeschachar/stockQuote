import os
from datetime import date

from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from dotenv import load_dotenv

import models
from database import engine, SessionLocal

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class PriceData(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    price: float
    volume: int
    latest_trading_day: date
    previous_close: float
    change: float
    change_percentage: float

    class Config:
        from_attributes = True


db = SessionLocal()
load_dotenv()

rapid_key = os.getenv('RAPID_API_KEY')


@app.get("/stock/quote")
def get_stock_quote(query_string=None):
    if query_string is None:
        query_string = {"function": "GLOBAL_QUOTE", "symbol": "MSFT", "datatype": "json"}
    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = query_string

    headers = {
        "X-RapidAPI-Key": f"{rapid_key}",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    quote_response = response.json()

    # Add data to DB
    db_quote_data = models.PriceData(
        symbol=quote_response["Global Quote"].get("01. symbol"),
        open=quote_response["Global Quote"].get("02. open"),
        high=quote_response["Global Quote"].get("03. high"),
        low=quote_response["Global Quote"].get("04. low"),
        price=quote_response["Global Quote"].get("05. price"),
        volume=quote_response["Global Quote"].get("06. volume"),
        latest_trading_day=quote_response["Global Quote"].get("07. latest trading day"),
        previous_close=quote_response["Global Quote"].get("08. previous close"),
        change=quote_response["Global Quote"].get("09. change"),
        change_percentage=quote_response["Global Quote"].get("10. change percent")
        )
    db.add(db_quote_data)
    db.commit()

    return quote_response


@app.get("/stock/price/{provided_symbol}/{provided_trading_day}")
async def get_stock_price(provided_symbol, provided_trading_day):
    result = db.query(models.PriceData).filter(
        models.PriceData.symbol == provided_symbol,
        models.PriceData.latest_trading_day == provided_trading_day
    ).all()
    if not result:
        raise HTTPException(status_code=404, detail='Symbol not found!')
    return result

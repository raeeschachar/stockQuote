from fastapi import FastAPI

app = FastAPI()


@app.get("/stock/quote")
def root():
    import requests

    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function": "GLOBAL_QUOTE", "symbol": "MSFT", "datatype": "json"}

    headers = {
        "X-RapidAPI-Key": "c4724e8bcdmsh4020992793038cep126cfcjsn8a30b8c08836",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    quote_response = response.json()
    return quote_response

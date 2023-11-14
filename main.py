from fastapi import FastAPI

app = FastAPI()


@app.get("/stock/quote")
def root():
    import requests

    url = "https://alpha-vantage.p.rapidapi.com/query"

    querystring = {"function": "GLOBAL_QUOTE", "symbol": "MSFT", "datatype": "json"}

    headers = {
        "X-RapidAPI-Key": "API-KEY",
        "X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    quote_response = response.json()
    return quote_response

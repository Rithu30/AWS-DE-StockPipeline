import requests

def fetch_stock(symbol, api_key):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"
    return requests.get(url).json()
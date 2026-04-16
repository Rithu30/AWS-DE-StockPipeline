import json
import boto3 # type: ignore
import urllib.request
import os
from datetime import datetime

s3 = boto3.client('s3')

BUCKET_NAME = "stock-data-raw-pipeline"
API_KEY = os.environ.get("API_KEY")

def lambda_handler(event, context):

    symbols = ["AAPL", "MSFT", "GOOGL"]
    data_list = []

    for symbol in symbols:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        data_list.append({
            "symbol": symbol,
            "price": data.get("c"),
            "timestamp": datetime.utcnow().isoformat()
        })

    now = datetime.utcnow()
    key = f"stock/year={now.year}/month={now.month}/day={now.day}/data.json"

    s3.put_object(
    Bucket=BUCKET_NAME,
    Key=key,
    Body="\n".join([json.dumps(record) for record in data_list])
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Data uploaded successfully")
    }
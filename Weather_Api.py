import requests
import pandas as pd
from datetime import datetime
import logging
import boto3
import os

logging.basicConfig(level=logging.INFO)

# ---- CONFIG ----
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
CITY = "Toronto"

S3_BUCKET = "weather-etl-bucket"
S3_PREFIX = "daily/weather"

OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
    f"?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
)

# ---- ETL ----


def run_etl():
    logging.info("Fetching weather data from OpenWeather API")

    response = requests.get(OPENWEATHER_URL)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame([{
        "city": CITY,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "timestamp": datetime.utcnow()
    }])

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_name = f"weather_data_{timestamp}.csv"
    local_path = f"/tmp/{file_name}"

    df.to_csv(local_path, index=False)
    logging.info(f"CSV written locally: {local_path}")

    s3_key = f"{S3_PREFIX}/{file_name}"
    s3 = boto3.client("s3")
    s3.upload_file(local_path, S3_BUCKET, s3_key)

    logging.info(f"Uploaded to s3://{S3_BUCKET}/{s3_key}")

    os.remove(local_path)
    logging.info("Local temp file cleaned up")

    return f"s3://{S3_BUCKET}/{s3_key}"


if __name__ == "__main__":
    run_etl()

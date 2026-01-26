# Weather Data ETL Pipeline using Apache Airflow on AWS

## Overview

This project demonstrates a **production-style ETL pipeline** built using **Apache Airflow on AWS EC2**.
The pipeline extracts live weather data from the **OpenWeather API**, transforms it using **Pandas**, and loads timestamped results into **Amazon S3** for historical analysis.

The goal of this project is to showcase:
- Airflow orchestration
- API-based data ingestion
- Cloud-native security using IAM roles
- AWS infrastructure automation readiness

---

## Architecture

```
OpenWeather API
      ↓
Apache Airflow (EC2)
      ↓
Python ETL (Pandas)
      ↓
Amazon S3 (timestamped CSV files)
```

---

## Key Features

- ⏱ Scheduled ETL using Apache Airflow DAG
- 🌐 External API data ingestion
- 🔄 Data transformation with Pandas
- ☁️ Secure upload to Amazon S3 using IAM Roles (no hardcoded keys)
- 🧾 Timestamped outputs for historical tracking
- 🛠 Runs on lightweight AWS EC2 (Ubuntu)

---

## Technology Stack

- Apache Airflow 2.8
- Python 3.10
- AWS EC2
- AWS S3
- IAM Roles
- Pandas
- Requests
- Boto3

---

## Project Structure

```
.
├── weather_etl.py              # ETL script (API → Pandas → S3)
├── airflow
│   └── dags
│       └── weather_etl_dag.py  # Airflow DAG
└── README.md
```

---

## ETL Flow

### 1. Extract
- Fetches current weather data from OpenWeather API
- Example city: Toronto

### 2. Transform
- Normalizes API response
- Adds UTC timestamp
- Converts data into a Pandas DataFrame

### 3. Load
- Writes CSV locally (temporary)
- Uploads file to S3 with timestamped filename
- Cleans up local temp file

Example S3 output:
```
s3://weather-etl-bucket/daily/weather/weather_data_20260125_183045.csv
```

---

## Airflow DAG

- **DAG ID:** `weather_api_etl`
- **Schedule:** Daily
- **Retries:** 2
- **Operator:** PythonOperator
- **Execution:** Runs the ETL script via subprocess

The DAG is automatically discovered by Airflow when placed in the `~/airflow/dags/` directory.

---

## AWS Security

- EC2 instance uses an **IAM Role** with S3 permissions
- No AWS access keys stored in code or configuration
- Uses instance metadata for secure credential management

---

## Setup Summary

1. Launch EC2 (Ubuntu)
2. Install Airflow inside a Python virtual environment
3. Disable Airflow example DAGs
4. Attach IAM role with S3 access to EC2
5. Add DAG to Airflow `dags/` directory
6. Start Airflow scheduler and webserver
7. Trigger DAG from Airflow UI

---

## How to Run

### Start Airflow (inside virtual environment)

```bash
airflow scheduler
```

```bash
airflow webserver --host 0.0.0.0 --port 8080 --workers 1
```

Access UI:
```
http://<EC2_PUBLIC_IP>:8080
```

Trigger the `weather_api_etl` DAG from the UI.

---

## Why This Design?

- **Simple but realistic**: Mirrors real-world ETL patterns without overengineering
- **Cloud-native**: Uses AWS IAM roles and S3
- **Interview-ready**: Clearly demonstrates orchestration, security, and data flow
- **Scalable**: Can be extended to MWAA, Glue, Parquet, or data warehouses

---

## Possible Enhancements

- Convert CSV output to Parquet
- Partition S3 data by date
- Add API retry & backoff logic
- Add data validation (Great Expectations)
- Migrate to Managed Workflows for Apache Airflow (MWAA)
- Add CloudWatch logging and alerts

---

## Author

Built as a learning and interview-focused project to demonstrate **Airflow-based ETL pipelines on AWS**.

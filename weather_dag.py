from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

def run_weather_etl():
    subprocess.run(
        ["python3", "/home/ubuntu/weather_etl.py"],
        check=True
    )

with DAG(
    dag_id="weather_api_etl",
    start_date=datetime.now(),
    schedule_interval="*/5 * * * *",
    catchup=False,
    default_args={"retries": 2},
) as dag:

    etl_task = PythonOperator(
        task_id="fetch_weather_data",
        python_callable=run_weather_etl,
    )
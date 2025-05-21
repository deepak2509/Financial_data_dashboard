from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath("/opt/airflow/etl_scripts"))


from extract import extract_data
from load_to_snowflake import load_data_to_snowflake

default_args = {
    'owner': 'deepak',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

with DAG(
    dag_id='crypto_elt_pipeline',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['crypto', 'ETL', 'Snowflake', 'dbt']
) as dag:

    extract_task = PythonOperator(
        task_id='extract_crypto_data',
        python_callable=extract_data
    )

    load_task = PythonOperator(
        task_id='load_to_snowflake',
        python_callable=load_data_to_snowflake
    )

    dbt_transform = BashOperator(
        task_id='run_dbt_models',
        bash_command='cd /Users/deepakgadde/Desktop/financial_data_pipeline/dbt_project'
    )

    extract_task >> load_task >> dbt_transform

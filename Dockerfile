# Dockerfile

FROM apache/airflow:2.8.1-python3.9

# Install dbt-core and dbt-snowflake
RUN pip install --no-cache-dir dbt-core dbt-snowflake

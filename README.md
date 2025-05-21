# 📈 Crypto Market ELT Pipeline & Dashboard

## CHECK MASTER BRANCH FOR CODE AND DOCUMENTATION
                                          -----DEEPAK GADDE

This project implements a full-stack ELT (Extract, Load, Transform) pipeline for tracking and visualizing real-time cryptocurrency market data using **CoinGecko API**, **Snowflake**, **dbt**, **Apache Airflow**, and **Power BI**.

---

## 🔧 Tech Stack

- **Data Extraction**: Python (CoinGecko API)
- **Data Loading**: Snowflake (via Python connector)
- **Data Transformation**: dbt (data models & staging)
- **Orchestration**: Apache Airflow (Docker-based setup)
- **Visualization**: Power BI (ODBC connector to Snowflake)

---

## 📦 Project Structure

financial_data_pipeline/
├── airflow/
│ ├── dags/
│ │ └── elt_dag.py # Airflow DAG for ELT
├── dbt_project/ # dbt transformations
├── etl_scripts/
│ ├── extract.py # Extract crypto data from API
│ └── load_to_snowflake.py # Load data into Snowflake
├── data/raw/ # Raw data storage (CSV)
├── docker-compose.yml # Airflow + Postgres setup
└── README.md # Project documentation

---

## ⚙️ Workflow

1. **Extract**: Python script hits CoinGecko API to fetch:
   - 30-day historical market charts
   - Coin metadata
   - Global market statistics

2. **Load**: Cleaned CSVs are loaded into **Snowflake** tables.

3. **Transform**: dbt creates staging models and combined views.

4. **Schedule**: Airflow DAG automates the full pipeline daily.

5. **Visualize**: Power BI connects directly to Snowflake to present key KPIs and interactive dashboards.

---

## 📊 Dashboards

**Power BI Dashboards include:**

- **KPI Cards**:
  - Total Coins Tracked
  - Avg. Daily Volume (30d)
  - Max Price (30d)
  - Lowest Market Cap Coin

- **Charts**:
  - Line Chart: Price trends by month & coin
  - Bar Chart: Volume_24h comparison across coins
  - Pie Chart: Market cap share by coin
  - Area Chart: Volume trend across time
  - Radar Chart: Developer & Community score comparison

---

## 🔑 Credentials

Make sure to set up your Snowflake credentials via environment variables or `.env` file.

```env
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_DATABASE=FINANCIAL_DB
SNOWFLAKE_SCHEMA=RAW
SNOWFLAKE_WAREHOUSE=NEWCOMPUTE_WH

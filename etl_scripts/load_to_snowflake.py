import os
import snowflake.connector
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# Environment variables for Snowflake
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")  # e.g. xy12345.us-east-1
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "NEWCOMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "FINANCIAL_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
print("USER:", os.getenv("SNOWFLAKE_USER"))
print("PWD:", os.getenv("SNOWFLAKE_PASSWORD"))
print("ACCOUNT:", os.getenv("SNOWFLAKE_ACCOUNT"))

# Local path to raw CSVs
RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/raw'))


def get_snowflake_connection():
    """Establish connection to Snowflake"""
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )


def create_table_from_df(cursor, df, table_name):
    """Create a Snowflake table dynamically based on DataFrame schema"""
    columns = ",\n".join([f'"{col}" STRING' for col in df.columns])
    ddl = f'CREATE OR REPLACE TABLE "{table_name}" (\n{columns}\n);'
    cursor.execute(ddl)
    print(f"[INFO] Created table: {table_name}")


def load_csv_to_table(file_path, table_name):
    """Load a CSV file into a Snowflake table"""
    print(f"[INFO] Loading {file_path} to table: {table_name}")
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        df = pd.read_csv(file_path)
        create_table_from_df(cursor, df, table_name)

        for i, row in df.iterrows():
            values = [str(v).replace("'", "''") for v in row.values]
            insert_sql = (
                f'INSERT INTO "{table_name}" VALUES ('
                + ", ".join([f"'{v}'" for v in values])
                + ");"
            )
            cursor.execute(insert_sql)

        print(f"[SUCCESS] Loaded {len(df)} rows into {table_name}")

    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {e}")
    finally:
        cursor.close()
        conn.close()


def load_data_to_snowflake():
    """Main function to load all raw files to Snowflake"""
    print("[INFO] Starting load to Snowflake...")

    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
    for file in files:
        table_name = os.path.splitext(file)[0].upper()
        load_csv_to_table(os.path.join(RAW_DIR, file), table_name)

    print("[INFO] Data loading completed.")


if __name__ == "__main__":
    load_data_to_snowflake()

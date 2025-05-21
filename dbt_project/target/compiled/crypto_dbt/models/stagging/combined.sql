-- models/staging/stg_all_crypto_prices.sql
SELECT * FROM FINANCIAL_DB.RAW.stg_crypto_prices
UNION ALL
SELECT * FROM FINANCIAL_DB.RAW.stg
UNION ALL
SELECT * FROM FINANCIAL_DB.RAW.solana
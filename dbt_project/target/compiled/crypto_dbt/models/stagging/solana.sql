SELECT
  'solana' AS coin,
  TRY_CAST("price_usd" AS FLOAT) AS price_usd,
  TRY_CAST("market_cap" AS FLOAT) AS market_cap,
  TRY_CAST("volume_24h" AS FLOAT) AS volume_24h,
  TRY_CAST("timestamp" AS TIMESTAMP) AS timestamp
FROM FINANCIAL_DB.RAW.SOLANA_MARKET_CHART
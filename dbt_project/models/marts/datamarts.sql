-- models/marts/mart_daily_crypto_summary.sql
SELECT
  coin,
  DATE_TRUNC('day', timestamp) AS date,
  AVG(price_usd) AS avg_price,
  MAX(price_usd) AS max_price,
  MIN(price_usd) AS min_price,
  AVG(volume_24h) AS avg_volume,
  AVG(market_cap) AS avg_market_cap
FROM {{ ref('combined') }}
GROUP BY 1, 2

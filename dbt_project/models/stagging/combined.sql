-- models/staging/stg_all_crypto_prices.sql
SELECT * FROM {{ ref('stg_crypto_prices') }}
UNION ALL
SELECT * FROM {{ ref('stg') }}
UNION ALL
SELECT * FROM {{ ref('solana') }}

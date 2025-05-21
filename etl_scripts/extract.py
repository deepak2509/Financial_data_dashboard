import requests
import os
import json
import pandas as pd
from datetime import datetime
import time

# Output directory
RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/raw'))
os.makedirs(RAW_DIR, exist_ok=True)


def fetch_market_chart(coin_id, vs_currency='usd', days='30'):
    """Fetch 30-day historical prices, volumes, and market caps"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}"
    response = requests.get(url)
    data = response.json()

    if "prices" not in data:
        print(f"[ERROR] 'prices' key not found in response for {coin_id}")
        print(json.dumps(data, indent=2))
        raise KeyError(f"[ERROR] API response missing 'prices' for {coin_id}")

    prices = pd.DataFrame(data["prices"], columns=["timestamp", "price_usd"])
    volumes = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume_24h"])
    market_caps = pd.DataFrame(data["market_caps"], columns=["timestamp", "market_cap"])

    df = prices.merge(volumes, on="timestamp").merge(market_caps, on="timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["coin"] = coin_id

    output_path = os.path.join(RAW_DIR, f"{coin_id}_market_chart.csv")
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved historical data for: {coin_id}")


def fetch_coin_metadata(coin_id):
    """Fetch detailed metadata for a cryptocurrency"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    response = requests.get(url)
    data = response.json()

    meta = {
        "coin": coin_id,
        "symbol": data.get("symbol"),
        "name": data.get("name"),
        "hashing_algorithm": data.get("hashing_algorithm"),
        "categories": ", ".join(data.get("categories", [])),
        "homepage": data.get("links", {}).get("homepage", [""])[0],
        "genesis_date": data.get("genesis_date"),
        "market_cap_rank": data.get("market_cap_rank"),
        "community_score": data.get("community_score"),
        "developer_score": data.get("developer_score"),
        "public_interest_score": data.get("public_interest_score"),
        "last_updated": data.get("last_updated"),
    }

    df = pd.DataFrame([meta])
    output_path = os.path.join(RAW_DIR, f"{coin_id}_metadata.csv")
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved metadata for: {coin_id}")


def fetch_global_stats():
    """Fetch global crypto market stats"""
    url = "https://api.coingecko.com/api/v3/global"
    response = requests.get(url)
    try:
        data = response.json()["data"]
    except KeyError:
        print("[ERROR] Global stats 'data' key missing. Full response:")
        print(json.dumps(response.json(), indent=2))
        return

    stats = {
        "total_market_cap_usd": data["total_market_cap"]["usd"],
        "total_volume_usd": data["total_volume"]["usd"],
        "market_cap_percentage_btc": data["market_cap_percentage"]["btc"],
        "market_cap_percentage_eth": data["market_cap_percentage"]["eth"],
        "active_cryptocurrencies": data["active_cryptocurrencies"],
        "markets": data["markets"],
        "updated_at": datetime.fromtimestamp(data["updated_at"]),
    }

    df = pd.DataFrame([stats])
    output_path = os.path.join(RAW_DIR, "global_crypto_stats.csv")
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved global market stats")


def extract_data():
    """Main ETL entrypoint for extraction"""
    print("[INFO] Starting complex CoinGecko extraction...")

    coin_ids = ["bitcoin", "ethereum", "solana", "ripple", "cardano"]

    for coin in coin_ids:
        try:
            fetch_market_chart(coin)
            time.sleep(2)
            fetch_coin_metadata(coin)
            time.sleep(2)
        except Exception as e:
            print(f"[WARNING] Skipping {coin} due to error: {e}")

    try:
        fetch_global_stats()
    except Exception as e:
        print(f"[WARNING] Global stats fetch failed: {e}")

    print("[INFO] CoinGecko extraction completed.")


if __name__ == "__main__":
    extract_data()

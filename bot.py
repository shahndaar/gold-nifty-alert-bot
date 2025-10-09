import os
import requests

# Fetch sensitive info from environment variables (GitHub Secrets)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MARKETSTACK_API_KEY = os.getenv("MARKETSTACK_API_KEY")
GOLD_API_KEY = os.getenv("GOLD_API_KEY")

def get_gold_price():
    url = "https://www.goldapi.io/api/XAU/INR"
    headers = {
        "x-access-token": "goldapi-4eg3smgj877cw-io",  # hardcoded for test
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if "price" not in data:
        raise ValueError(f"Error fetching gold price from GoldAPI.io: {data}")
    price_per_ounce_in_inr = data["price"]
    price_per_gram_in_inr = price_per_ounce_in_inr / 31.1035  # Troy ounce to gram
    return round(price_per_gram_in_inr * 1.10, 2)

def get_nifty_price():
    url = f"https://api.marketstack.com/v2/eod/latest?access_key={MARKETSTACK_API_KEY}&symbols=^NSEI"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise ValueError(f"Error fetching data from MarketStack API: {e}")

    try:
        return float(data["data"][0]["close"])
    except (IndexError, KeyError) as e:
        raise ValueError(f"Error parsing Nifty price from response: {data}") from e

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def main():
    gold_price = get_gold_price()
    nifty_price = get_nifty_price()
    ratio = gold_price / nifty_price

    message = (
        f"💰 Gold Price (₹/gm): {gold_price}\n"
        f"📈 Nifty Price: {nifty_price}\n"
        f"🔢 Gold/Nifty Ratio: {ratio:.4f}\n"
    )

    if ratio >= 0.600:
        message += "⚠️ Sell Equities and Buy Gold\n"
    elif ratio <= 0.280:
        message += "⚠️ Sell Gold and Buy Equities\n"
    else:
        message += "✅ No action needed\n"

    send_message(message)

if __name__ == "__main__":
    main()

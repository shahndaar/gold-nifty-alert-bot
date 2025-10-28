import requests

# Your Telegram bot token and chat ID
import os
TOKEN = "7720062392:AAE3ciawKeDce8ruQGbOyjlg16pkNlkUiKQ"
CHAT_ID = "6884123314"
MARKETSTACK_API_KEY = "3010bdc7607fff414231a83b49f8f26b"
GOLD_API_KEY = "goldapi-4eg3smgj877cw-io"

print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)

def get_gold_price():
    import os
    api_key = "goldapi-4eg3smgj877cw-io"
    url = "https://www.goldapi.io/api/XAU/INR"
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    # goldapi gives price per troy ounce in INR
    price_per_ounce_in_inr = data["price"]
    price_per_gram_in_inr = price_per_ounce_in_inr / 31.1035  # Troy ounce to gram
    return round(price_per_gram_in_inr*1.10, 2)

def get_nifty_price():
    import os
    import requests

    api_key = "3010bdc7607fff414231a83b49f8f26b"
    url = fhttps://www.alphavantage.co/query?symbol=NSE:NIFTYBEES.NS&apikey=RSZ90VYQTLKNPPSE"
    # url = f"https://api.marketstack.com/v2/eod/latest?access_key={api_key}&symbols=^NSEI"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()
        print("MarketStack response data:", data)
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

    # Updated alerts based on ratio
    if ratio >= 0.600:
        message += "⚠️ Sell Equities and Buy Gold\n"
    elif ratio <= 0.280:
        message += "⚠️ Sell Gold and Buy Equities\n"
    else:
        message += "✅ No action needed\n"

    send_message(message)

if __name__ == "__main__":
    main()

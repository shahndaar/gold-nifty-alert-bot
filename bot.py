import requests

# Your Telegram bot token and chat ID
import os
TOKEN = "7720062392:AAE3ciawKeDce8ruQGbOyjlg16pkNlkUiKQ"
CHAT_ID = "6884123314"
ALPHA_API_KEY = "1OBJS4GR777951LD"

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

import requests
import os

def get_nifty_price():
    api_key = ALPHA_API_KEY
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=NSEI&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    print("Alpha Vantage response:", data)  # Debug print to check the actual returned data

    try:
        price = float(data["Global Quote"]["05. price"])
        return price
    except KeyError:
        raise ValueError(f"Error fetching Nifty price from Alpha Vantage API. Response: {data}")


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

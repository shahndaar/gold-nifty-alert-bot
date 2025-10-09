import requests

# Your Telegram bot token and chat ID
import os
TOKEN = 7720062392:AAE3ciawKeDce8ruQGbOyjlg16pkNlkUiKQ
CHAT_ID = 6884123314

print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)

def get_gold_price():
    # Using free API or workaround to get gold price in INR per gram
    # For demonstration, we'll use a placeholder price, replace with your API later
    gold_price_inr_per_gram = 6000  # Replace with real API call
    return gold_price_inr_per_gram

def get_nifty_price():
    # Using Yahoo Finance unofficial API for Nifty example
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=^NSEI"
    response = requests.get(url)
    data = response.json()
    nifty_price = data['quoteResponse']['result'][0]['regularMarketPrice']
    return nifty_price

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

    # Add alerts for your specific ratio levels here
    if ratio > 8:  # example upper threshold
        message += "⚠️ Ratio above 8 - consider action!\n"
    elif ratio < 6:  # example lower threshold
        message += "⚠️ Ratio below 6 - consider action!\n"

    send_message(message)

if __name__ == "__main__":
    main()

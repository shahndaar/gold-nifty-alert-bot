import requests

# Your Telegram bot token and chat ID
import os
TOKEN = "7720062392:AAE3ciawKeDce8ruQGbOyjlg16pkNlkUiKQ"
CHAT_ID = "6884123314"

print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)

def get_gold_price():
    # Example with Metals-API (requires free API key signup)
    url = "https://metals-api.com/api/latest?access_key=YOUR_API_KEY&base=INR&symbols=XAU"
    response = requests.get(url)
    data = response.json()
    # XAU price per troy ounce in INR
    rate_per_ounce_in_inr = data["rates"]["XAU"]
    # Convert per ounce to per gram (1 troy ounce = 31.1035 grams)
    rate_per_gram_in_inr = rate_per_ounce_in_inr / 31.1035
    return round(rate_per_gram_in_inr, 2)

def get_nifty_price():
    url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=^NSEI"
    response = requests.get(url)
    print("Nifty response status code:", response.status_code)
    print("Nifty response text:", response.text)
    try:
        data = response.json()
        if (
            "quoteResponse" in data
            and "result" in data["quoteResponse"]
            and len(data["quoteResponse"]["result"]) > 0
        ):
            return data["quoteResponse"]["result"][0]["regularMarketPrice"]
        else:
            print("Yahoo Finance API missing data, fallback value used")
            return 20000  # Fallback, replace with real value if you want
    except Exception as e:
        print("Yahoo Finance API error:", str(e))
        return 20000  # Fallback value

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

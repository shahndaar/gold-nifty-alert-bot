import os
import requests
import datetime
import io
import matplotlib.pyplot as plt

# Constants - embed your keys here
TOKEN = "7720062392:AAE3ciawKeDce8ruQGbOyjlg16pkNlkUiKQ"
CHAT_ID = "6884123314"
MARKETSTACK_KEY = "3010bdc7607fff414231a83b49f8f26b"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    resp = requests.post(url, data=payload)
    if resp.status_code != 200:
        print("Error sending message:", resp.text)
    return resp.json()

def send_chart_image(image_buffer):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    files = {'photo': ('chart.png', image_buffer)}
    data = {'chat_id': CHAT_ID, 'caption': 'Gold/Nifty Ratio Last 7 Days (Hourly)'}
    response = requests.post(url, files=files, data=data)
    if response.status_code != 200:
        print("Error sending photo:", response.text)
    return response.json()

def get_gold_price():
    # Fetch current gold price from MarketStack commodities (gold)
    url = f"https://api.marketstack.com/v2/commodities?access_key={MARKETSTACK_KEY}&commodity_name=gold"
    resp = requests.get(url)
    data = resp.json()
    if "data" in data and len(data["data"]) > 0:
        price = float(data["data"][0]["commodity_price"])
        return price
    else:
        raise ValueError(f"Error fetching gold price: {data}")

def get_nifty_price():
    url = f"https://api.marketstack.com/v2/eod/latest?access_key={MARKETSTACK_KEY}&symbols=^NSEI"
    response = requests.get(url)
    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        return float(data['data'][0]['close'])
    else:
        raise ValueError(f"Error fetching Nifty price: {data}")

def fetch_historical_prices(symbol, limit=168):
    # Fetch last 'limit' hours of hourly intraday data for the symbol
    url = f"https://api.marketstack.com/v2/intraday?access_key={MARKETSTACK_KEY}&symbols={symbol}&interval=1hour&limit={limit}"
    resp = requests.get(url)
    data = resp.json()
    if 'data' in data and len(data['data']) > 0:
        # Sort by date ascending
        sorted_data = sorted(data['data'], key=lambda x: x['date'])
        return [float(item['close']) for item in sorted_data]
    else:
        raise ValueError(f"Error fetching historical prices for {symbol}: {data}")

def plot_ratio_chart(gold_prices, nifty_prices):
    ratio = [g / n for g, n in zip(gold_prices, nifty_prices)]
    plt.figure(figsize=(10, 6))
    plt.plot(ratio, label="Gold/Nifty Ratio", color="purple")
    plt.xlabel("Hours (last 7 days)")
    plt.ylabel("Ratio")
    plt.title("Gold to Nifty Ratio - Last 7 Days (Hourly)")
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def send_alert_message(gold_price, nifty_price, ratio):
    message = (
        f"💰 Gold Price (₹/gm): {gold_price:.2f}\n"
        f"📈 Nifty Price: {nifty_price:.2f}\n"
        f"🔢 Gold/Nifty Ratio: {ratio:.4f}\n"
    )
    if ratio >= 0.600:
        message += "⚠️ Sell Equities and Buy Gold"
    elif ratio <= 0.280:
        message += "⚠️ Sell Gold and Buy Equities"
    else:
        message += "✅ No action needed"
    send_message(message)

def main():
    # Only run Monday-Friday
    weekday = datetime.datetime.utcnow().weekday()  # Monday=0, Sunday=6
    if weekday > 4:  # Sat/Sun do not run
        print("Weekend - no alert sent")
        return

    # Fetch prices
    gold_price = get_gold_price()
    nifty_price = get_nifty_price()
    ratio = gold_price / nifty_price

    send_alert_message(gold_price, nifty_price, ratio)

    # Current UTC hour to detect if last run of day (9:00 UTC = 2:30 PM IST)
    current_utc_hour = datetime.datetime.utcnow().hour
    # Send chart image only on last run at 9:00 UTC
    if current_utc_hour == 9:
        gold_prices = fetch_historical_prices('GOLD', 168)  # 7 days * 24 hours
        nifty_prices = fetch_historical_prices('^NSEI', 168)
        chart_buf = plot_ratio_chart(gold_prices, nifty_prices)
        send_chart_image(chart_buf)


if __name__ == "__main__":
    main()

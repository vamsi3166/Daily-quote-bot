import os
import random
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Used only if the live API call fails, so the daily message never silently skips
FALLBACK_QUOTES = [
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Hardships often prepare ordinary people for an extraordinary destiny.", "C.S. Lewis"),
    ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
    ("What lies behind us and what lies before us are tiny matters compared to what lies within us.", "Ralph Waldo Emerson"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
]


def get_quote():
    """Fetch a random quote from ZenQuotes; fall back to a local list on any failure."""
    try:
        resp = requests.get("https://zenquotes.io/api/random", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        quote_text = data[0]["q"]
        author = data[0]["a"]
        return quote_text, author
    except Exception as e:
        print(f"API fetch failed, using fallback quote instead: {e}")
        return random.choice(FALLBACK_QUOTES)


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    resp = requests.post(url, data=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


def main():
    quote, author = get_quote()
    message = f"🌅 <b>Daily Motivation</b>\n\n\"{quote}\"\n\n— {author}"
    result = send_telegram_message(message)
    print("Message sent successfully:", result.get("ok"))


if __name__ == "__main__":
    main()

import os
import asyncio
import feedparser
from flask import Flask
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
PORT = int(os.getenv("PORT", 10000))

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "RSS Test Bot LIVE"

RSS_URL = "https://www.investing.com/rss/news_301.rss"

async def test_rss():

    print("🚀 Test RSS avviato")

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        print("❌ Nessuna news trovata")
        return

    entry = feed.entries[0]

    message = (
        f"🧪 TEST RSS\n\n"
        f"{entry.title}\n\n"
        f"{entry.link}"
    )

    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print("✅ Messaggio inviato")

    except Exception as e:
        print("❌ ERRORE TELEGRAM:", e)


if __name__ == "__main__":

    from threading import Thread

    def start_test():
        asyncio.run(test_rss())

    Thread(target=start_test).start()

    app.run(host="0.0.0.0", port=PORT)

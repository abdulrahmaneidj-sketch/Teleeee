import os
import logging
import time
from openai import OpenAI
import telebot

# ---------- Configuration ----------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logging.error("Missing TELEGRAM_TOKEN or OPENAI_API_KEY environment variables. Exiting.")
    raise SystemExit("Missing TELEGRAM_TOKEN or OPENAI_API_KEY environment variables.")

# Initialize clients
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
client = OpenAI(api_key=OPENAI_API_KEY)

# Helper: extract text from OpenAI response robustly
def extract_reply(response):
    try:
        # Preferred path (object style)
        choice = response.choices[0]
        # If the SDK returns a 'message' object with .content
        if hasattr(choice, "message") and getattr(choice.message, "content", None):
            return choice.message.content
        # Fallback to dictionary access
        if isinstance(choice, dict):
            return choice.get("message", {}).get("content") or choice.get("text")
        # Last resort
        return str(response)
    except Exception:
        return str(response)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = (
        "مرحبًا 👋\n"
        "أنا بوت شرح تخطيط القلب (ECG with Abu Eid).\n"
        "أرسل نصًا أو سؤالاً عن ECG وسأرد باختصار وبدقة.\n"
        "إذا احتجت مساعدة أرسل /help."
    )
    bot.reply_to(message, text)

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message):
    user_text = message.text.strip()
    if not user_text:
        bot.reply_to(message, "أرسل نص واضح وسأجاوبك.")
        return

    logging.info("Message from %s: %.80s", getattr(message.from_user, "username", message.from_user.id), user_text)
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        # Call OpenAI (chat completion)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant specialized in ECG (electrocardiography). Answer concisely and accurately. If the user writes in Arabic, reply in Arabic; if in English, reply in English."},
                {"role": "user", "content": user_text}
            ],
            max_tokens=600
        )

        reply = extract_reply(response)
        # safety fallback
        if not reply or reply.strip() == "":
            reply = "عذرًا، لم أتمكن من توليد إجابة واضحة الآن. حاول مرة ثانية."
        bot.reply_to(message, reply)

    except Exception as e:
        logging.exception("Failed to process message")
        # do not leak internal errors or API keys to end-users
        bot.reply_to(message, "حصل خطأ داخلي أثناء معالجة الطلب. تأكد من إعداد المتغيرات (TELEGRAM_TOKEN & OPENAI_API_KEY) ومن أن رصيد OpenAI كافٍ.")

if __name__ == '__main__':
    # Keep the bot running and auto-restart on crashes with a short backoff
    backoff = 1
    while True:
        try:
            logging.info("Starting Telegram polling...")
            # infinity_polling will attempt to reconnect automatically for many exceptions
            bot.infinity_polling(timeout=20, long_polling_timeout=30)
        except Exception:
            logging.exception("Polling crashed — restarting after %s seconds", backoff)
            time.sleep(backoff)
            backoff = min(backoff * 2, 60)

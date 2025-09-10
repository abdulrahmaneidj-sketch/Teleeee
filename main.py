import telebot
import os
from openai import OpenAI

# قراءة المتغيرات من Railway Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# إنشاء عملاء التليقرام والـ OpenAI
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text

    try:
        # استخدام gpt-3.5-turbo-instruct
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=user_message,
            max_tokens=500
        )

        reply = response.choices[0].text.strip()
        bot.reply_to(message, reply if reply else "ما وصلني رد من الذكاء الاصطناعي.")

    except Exception as e:
        bot.reply_to(message, f"صار خطأ: {str(e)}")

print("البوت شغال...")
bot.infinity_polling()

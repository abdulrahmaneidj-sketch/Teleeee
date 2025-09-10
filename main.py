import os
import telebot
import google.generativeai as genai

# Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Telegram bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

@bot.message_handler(func=lambda message: True)
def reply_to_user(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"خطأ: {e}")

print("البوت شغال مع Gemini ...")
bot.polling()

import os
import telebot
import google.generativeai as genai

# 🟢 جلب المتغيرات من Railway Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 🟢 تهيئة التوكنات
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# 🟢 اختيار موديل Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

# 🟢 استقبال أي رسالة من المستخدم
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        prompt = message.text
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"آسف، صار خطأ: {e}")

# 🟢 تشغيل البوت
print("✅ البوت شغال ...")
bot.infinity_polling()

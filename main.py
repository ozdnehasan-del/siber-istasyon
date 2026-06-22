import telebot
from telebot import types
import whois
import os

TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚨 İhbar Et")
    btn2 = types.KeyboardButton("🔍 IP Analiz")
    btn3 = types.KeyboardButton("📝 Dilekçe")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "💀 SİBER İSTASYON v19 AKTİF\n\nİşlem seç:", reply_markup=markup)

@bot.message_handler(commands=['whois'])
def whois_sorgu(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "Örnek kullanım: /whois google.com")
        return
    site = parts[1]
    try:
        data = whois.whois(site)
        bot.reply_to(message, str(data))
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "🚨 İhbar Et":
        bot.reply_to(message, "🚨 İhbar paneline yönlendiriliyorsun...")
    elif message.text == "🔍 IP Analiz":
        bot.reply_to(message, "🔍 Lütfen analiz edilecek IP adresini yaz:")
    elif message.text == "📝 Dilekçe":
        bot.reply_to(message, "📝 Dilekçe taslağı oluşturuluyor...")
    else:
        bot.reply_to(message, "Anlaşılamadı, lütfen menüdeki butonları kullan.")

bot.polling()

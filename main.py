import telebot
import whois
import os

TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "💀 SİBER İSTASYON v19 AKTİF (BULUT MOD)")

@bot.message_handler(commands=['whois'])
def whois_sorgu(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Örn: /whois google.com")
            return
        site = parts[1]
        w = whois.whois(site)
        rapor = f"🌐 {w.domain_name}\n🏢 {w.registrar}\n📍 {w.country}"
        bot.send_message(message.chat.id, rapor)
    except Exception as e:
        bot.reply_to(message, "Hata oluştu.")

bot.infinity_polling()


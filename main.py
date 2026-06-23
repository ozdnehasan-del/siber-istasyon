import telebot
from telebot import types
import requests
import socket
import whois

TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
bot = telebot.TeleBot(TOKEN)

# 1. URL INSPECTOR MODÜLÜ (Örnek Modül)
def analiz_url(url):
    try:
        r = requests.get(url, timeout=5)
        return f"🌐 *URL Analizi*\nTarget: {r.url}\nStatus: {r.status_code}\nServer: {r.headers.get('Server', 'Bilinmiyor')}"
    except Exception as e:
        return f"❌ Hata: {str(e)}"

# 2. IP ANALİZ MODÜLÜ
def analiz_ip(ip):
    try:
        # Gerçek bir API üzerinden IP lokasyon bilgisi çekme (ip-api.com)
        r = requests.get(f"http://ip-api.com/json/{ip}").json()
        if r['status'] == 'success':
            return f"📍 *IP Analizi*\nÜlke: {r['country']}\nŞehir: {r['city']}\nISP: {r['isp']}"
        return "❌ IP bilgisi bulunamadı."
    except Exception as e:
        return f"❌ Hata: {str(e)}"

# --- BOT ARAYÜZÜ ---
@bot.message_handler(commands=['start'])
def start(message):
    msg = (
        "🚀 *Vesk-OSINT İstihbarat toplamaya hoş geldiniz.*\n"
        "Sistem aktif. Hedef analizi için aşağıdaki paneli kullanın."
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Butonlar
    markup.add(
        types.InlineKeyboardButton("🌐 URL Analiz", callback_data="do_url"),
        types.InlineKeyboardButton("📍 IP Analiz", callback_data="do_ip")
    )
    bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "do_url":
        msg = bot.send_message(call.message.chat.id, "🔗 Analiz edilecek URL'yi girin (http ile):")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, analiz_url(m.text), parse_mode="Markdown"))
    elif call.data == "do_ip":
        msg = bot.send_message(call.message.chat.id, "📍 Analiz edilecek IP adresini girin:")
        bot.register_next_step_handler(msg, lambda m: bot.reply_to(m, analiz_ip(m.text), parse_mode="Markdown"))

if __name__ == "__main__":
    bot.infinity_polling()

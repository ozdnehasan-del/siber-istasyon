import telebot
from telebot import types
import requests
import whois
import socket
import os
from flask import Flask
from threading import Thread

# --- TOKEN (GÜNCEL) ---
TOKEN = '8873167036:AAH9BXyAgNqwbwY0jthyEbDh189yOSqPNWE'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SUNUCUSU ---
@app.route('/')
def home():
    return "Vesk-OSINT Botu Aktif!"

def run_server(port):
    app.run(host='0.0.0.0', port=port)

# --- ANA MENÜ ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🌐 URL Analiz", callback_data="do_url"),
        types.InlineKeyboardButton("📍 IP Analiz", callback_data="do_ip"),
        types.InlineKeyboardButton("🔍 Domain/Whois", callback_data="do_domain")
    )
    return markup

# --- START KOMUTU ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 *Vesk-OSINT Paneline Hoş Geldiniz.*", parse_mode="Markdown")
    bot.send_message(message.chat.id, "İstediğiniz analizi aşağıdan seçin:", reply_markup=ana_menu(), parse_mode="Markdown")

# --- CALLBACK İŞLEMLERİ ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "do_url":
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔗 URL'yi girin (http ile):")
        bot.register_next_step_handler(msg, link_analiz_islem)
    elif call.data == "do_ip":
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📍 IP adresini girin:")
        bot.register_next_step_handler(msg, ip_analiz_islem)
    elif call.data == "do_domain":
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔍 Domaini girin (örn: google.com):")
        bot.register_next_step_handler(msg, domain_analiz_islem)

# --- ANALİZ FONKSİYONLARI ---
def link_analiz_islem(message):
    try:
        r = requests.get(message.text, timeout=10)
        rapor = f"🌐 *URL Analizi*\nTarget: {r.url}\nStatus: {r.status_code}\nServer: {r.headers.get('Server', 'Bilinmiyor')}"
    except Exception as e:
        rapor = f"❌ Hata: {str(e)}"
    bot.send_message(message.chat.id, rapor, parse_mode="Markdown", reply_markup=ana_menu())

def ip_analiz_islem(message):
    try:
        r = requests.get(f"http://ip-api.com/json/{message.text}", timeout=10).json()
        if r.get('status') == 'success':
            rapor = f"📍 *IP Analizi*\nÜlke: {r['country']}\nŞehir: {r['city']}\nISP: {r['isp']}"
        else:
            rapor = "❌ IP bilgisi bulunamadı."
    except Exception as e:
        rapor = f"❌ Hata: {str(e)}"
    bot.send_message(message.chat.id, rapor, parse_mode="Markdown", reply_markup=ana_menu())

def domain_analiz_islem(message):
    domain = message.text
    try:
        w = whois.whois(domain)
        ip = socket.gethostbyname(domain)
        rapor = (f"🔍 *Domain: {domain}*\n📍 IP: `{ip}`\n📅 Kayıt: {str(w.creation_date)}\n🏢 Firma: {str(w.registrar)}")
    except Exception as e:
        rapor = f"❌ Hata: {str(e)}"
    bot.send_message(message.chat.id, rapor, parse_mode="Markdown", reply_markup=ana_menu())

# --- BAŞLATICI ---
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    t = Thread(target=run_server, args=(port,))
    t.daemon = True
    t.start()
    bot.infinity_polling()

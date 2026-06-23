import telebot
from telebot import types
import requests
import whois
import socket

# Yeni Token'ın yerleştirildi
TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
bot = telebot.TeleBot(TOKEN)

# --- ANA MENÜ ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🌐 URL Analiz", callback_data="do_url"),
        types.InlineKeyboardButton("📍 IP Analiz", callback_data="do_ip"),
        types.InlineKeyboardButton("🔍 Domain/Whois", callback_data="do_domain")
    )
    return markup

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    try:
        remove_markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "🚀 *Vesk-OSINT İstihbarat toplamaya hoş geldiniz.*", reply_markup=remove_markup, parse_mode="Markdown")
        bot.send_message(message.chat.id, "Sistem aktif. Hedef analizi için paneli kullanın:", reply_markup=ana_menu(), parse_mode="Markdown")
    except Exception as e:
        print(f"Start hatası: {e}")

# --- CALLBACK ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.data == "do_url":
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔗 Analiz edilecek URL'yi girin (http ile):")
            bot.register_next_step_handler(msg, link_analiz_islem)
        elif call.data == "do_ip":
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📍 Analiz edilecek IP adresini girin:")
            bot.register_next_step_handler(msg, ip_analiz_islem)
        elif call.data == "do_domain":
            msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🔍 Analiz edilecek domaini girin (örn: google.com):")
            bot.register_next_step_handler(msg, domain_analiz_islem)
    except Exception as e:
        print(f"Callback hatası: {e}")

# --- İŞLEMCİLER ---
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

# Hata toleranslı polling
if __name__ == "__main__":
    print("Bot başlatılıyor...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- AYARLAR ---
TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
ADMIN_USERNAME = "@vesk" 
bot = telebot.TeleBot(TOKEN)

# --- WEB SUNUCUSU (Uyumaması İçin) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Vesk Bot Aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- MENÜLER ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 Ad Soyad Sorgu", callback_data="sorgu_yok"),
        types.InlineKeyboardButton("🆔 T.C. Sorgu", callback_data="sorgu_yok"),
        types.InlineKeyboardButton("📱 GSM/TC Sorgu", callback_data="sorgu_yok"),
        types.InlineKeyboardButton("🏠 Adres Sorgu", callback_data="sorgu_yok"),
        types.InlineKeyboardButton("📂 Tüm Sorgular (Full)", callback_data="sorgu_listesi"),
        types.InlineKeyboardButton("💎 VIP Satın Al", callback_data="vip_bilgi")
    )
    return markup

def sorgu_paneli_genis():
    markup = types.InlineKeyboardMarkup(row_width=2)
    butonlar = [
        "💳 Iban Sorgu", "👨‍👩‍👧 Aile Detaylı", "🏠 Hane Sorgu", "🧒 Yeğen Sorgu",
        "👶 Çocuk Sorgu", "👵 Kızlık Soyadı", "📂 Sicil Sorgu", "⚖️ Mahkum Sorgu",
        "🎓 Üniversite Sorgu", "🏢 İşyeri Sorgu", "🚗 Araç Muayene", "🚙 Plaka Sorgu",
        "📜 Tapu Sorgu", "🗺️ Ada Parsel", "🌳 Soyağacı Sorgu", "🏥 Muayene Sorgu",
        "🗓️ Skt Tarihi", "🌐 Ip Adresi Sorgu", "🖼️ Vesika Sorgu", "💊 İlaç Sorgu",
        "📞 Türk Telekom Fatura", "📍 Anlık Konum", "📹 Kamera Sızma", "📸 Instagram Hack",
        "👥 Facebook Hack", "🕊️ Yetimlik Sorgu", "👤 Soyisimsiz Sorgu", "💻 Casus Yazılım",
        "💣 Sms Saldırısı"
    ]
    for text in butonlar:
        markup.add(types.InlineKeyboardButton(text, callback_data="sorgu_yok"))
    markup.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="ana_menu"))
    return markup

# --- KOMUTLAR ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 *VESK SORGU PANELİ*\nHoş geldin! İşlem seç:", reply_markup=ana_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "sorgu_listesi":
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📁 *VIP Sorgu Listesi Açıldı*\nLütfen sorgu türünü seçin:", reply_markup=sorgu_paneli_genis(), parse_mode="Markdown")
        except: pass
    elif call.data == "ana_menu":
        try:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🚀 *VESK SORGU PANELİ*\nİşlem seçiniz:", reply_markup=ana_menu(), parse_mode="Markdown")
        except: pass
    elif call.data == "sorgu_yok":
        bot.answer_callback_query(call.id, "⚠️ VIP Gerekli!")
        bot.send_message(call.message.chat.id, f"❌ *SORGULAMA BAŞARISIZ!*\n\n💎 *VIP ÖZEL SATIN ALIM İÇİN {ADMIN_USERNAME}*", parse_mode="Markdown")
    elif call.data == "vip_bilgi":
        bot.send_message(call.message.chat.id, f"💎 *VIP ÜYELİK AVANTAJLARI*\n\n✅ Tüm sorgular sınırsız.\n✅ SMS Bombing & Casus Yazılım aktif.\n\n💰 Satın almak için: {ADMIN_USERNAME}", parse_mode="Markdown")

# --- BOTU BAŞLAT ---
if __name__ == "__main__":
    keep_alive() # Web sunucusunu başlat
    bot.infinity_polling() # Botu başlat

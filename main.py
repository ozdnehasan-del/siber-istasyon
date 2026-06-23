import telebot
from telebot import types
from flask import Flask
from threading import Thread
import random
import os
import time

# --- AYARLAR ---
TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
ADMIN_USERNAME = "@veskbaba"
ADMIN_ID = "123456789" # Buraya kendi sayısal ID'ni yaz!
bot = telebot.TeleBot(TOKEN)

# --- SİMÜLASYON İŞLEVLERİ ---
def simule_et(message, islem):
    msg = bot.send_message(message.chat.id, f"🔍 {islem} başlatılıyor...")
    time.sleep(1.5)
    bot.edit_message_text(f"🔐 {islem} verileri işleniyor...", message.chat.id, msg.message_id)
    time.sleep(1.5)

def insta_hack(message):
    simule_et(message, "Instagram Hack")
    bot.send_message(message.chat.id, f"✅ @{message.text} analiz edildi.\n🔑 Şifre: **{random.randint(100000, 999999)}**\n💎 Destek: {ADMIN_USERNAME}")

def plaka_sorgu(message):
    simule_et(message, "Plaka Sorgu")
    tc = "".join([str(random.randint(0, 9)) for _ in range(11)])
    bot.send_message(message.chat.id, f"🚗 Plaka: {message.text.upper()}\n👤 Sahibi: {random.choice(['Ahmet Yılmaz', 'Ayşe Kaya', 'Mehmet Demir'])}\n🆔 TC: {tc}\n💎 Destek: {ADMIN_USERNAME}")

def casus_yazilim(message):
    bot.send_message(message.chat.id, "🔗 Bağlantı oluşturuluyor...")
    time.sleep(2)
    bot.send_message(message.chat.id, f"🌐 Link: https://global-izleme.com/capture?id={random.randint(1000,9999)}\n⚠️ Destek: {ADMIN_USERNAME}")

def dosya_hazirla(message):
    bot.send_message(message.chat.id, "📂 10.000 kişilik liste hazırlanıyor...")
    dosya_adi = "Sorgu_Sonuclari.txt"
    with open(dosya_adi, "w", encoding="utf-8") as f:
        for i in range(10000):
            tc = "".join([str(random.randint(0, 9)) for _ in range(11)])
            f.write(f"Kullanıcı_{i} | TC: {tc} | Durum: Aktif\n")
    with open(dosya_adi, "rb") as doc:
        bot.send_document(message.chat.id, doc)
    os.remove(dosya_adi)

# --- WEB ---
app = Flask(__name__)
@app.route('/')
def home(): return "Vesk Bot Aktif!"
def keep_alive(): Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# --- MENÜLER ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 Ad Soyad Sorgu", callback_data="sorgu_input"),
        types.InlineKeyboardButton("📂 Tüm Sorgular (Full)", callback_data="sorgu_listesi"),
        types.InlineKeyboardButton(f"💎 VIP Satın Al ({ADMIN_USERNAME})", callback_data="vip_bilgi")
    )
    return markup

def sorgu_paneli_genis():
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Görsellerdeki tüm butonların listesi
    butonlar = [
        ("💳 Iban Sorgu", "sim_islem"), ("👨‍👩‍👧 Aile Detaylı", "sim_islem"),
        ("🏠 Hane Sorgu", "sim_islem"), ("🧒 Yeğen Sorgu", "sim_islem"),
        ("👶 Çocuk Sorgu", "sim_islem"), ("👵 Kızlık Soyadı", "sim_islem"),
        ("📂 Sicil Sorgu", "sim_islem"), ("⚖️ Mahkum Sorgu", "sim_islem"),
        ("🎓 Üniversite Sorgu", "sim_islem"), ("🏢 İşyeri Sorgu", "sim_islem"),
        ("🚗 Araç Muayene", "sim_islem"), ("🚙 Plaka Sorgu", "plaka_gir"),
        ("📜 Tapu Sorgu", "sim_islem"), ("🗺️ Ada Parsel", "sim_islem"),
        ("🌳 Soyağacı Sorgu", "sim_islem"), ("🏥 Muayene Sorgu", "sim_islem"),
        ("🗓️ Skt Tarihi", "sim_islem"), ("🌐 Ip Adresi Sorgu", "sim_islem"),
        ("🖼️ Vesika Sorgu", "sim_islem"), ("💊 İlaç Sorgu", "sim_islem"),
        ("📞 Türk Telekom Fatura", "sim_islem"), ("📍 Anlık Konum", "sim_islem"),
        ("📹 Kamera Sızma", "sim_islem"), ("📸 Instagram Hack", "insta_gir"),
        ("👥 Facebook Hack", "sim_islem"), ("🕊️ Yetimlik Sorgu", "sim_islem"),
        ("👤 Soyisimsiz Sorgu", "soyisim_baslat"), ("💻 Casus Yazılım", "casus_baslat"),
        ("💣 Sms Saldırısı", "sim_islem"), ("🏫 Sınıf Sorgu", "sim_islem"),
        ("📜 Seri No Sorgu", "sim_islem"), ("🏢 Mersis Dükkan", "sim_islem")
    ]
    for text, cd in butonlar: markup.add(types.InlineKeyboardButton(text, callback_data=cd))
    markup.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="ana_menu"))
    return markup

# --- KOMUTLAR ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 *VESK SORGU PANELİ*\nİşlem seç:", reply_markup=ana_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "sorgu_input":
        msg = bot.send_message(call.message.chat.id, "🔍 Sorgulanacak ismi yaz:")
        bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, f"Sonuç: {random.choice(['Bulundu', 'Bulunamadı'])}"))
    elif call.data == "sorgu_listesi":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📁 *VİP SORGULAR*", reply_markup=sorgu_paneli_genis(), parse_mode="Markdown")
    elif call.data == "vip_bilgi":
        bot.send_message(call.message.chat.id, f"💎 *VIP ÜYELİK*\nSatın almak için: {ADMIN_USERNAME} ile iletişime geçin.")
    elif call.data == "plaka_gir":
        msg = bot.send_message(call.message.chat.id, "🚗 Plaka giriniz:")
        bot.register_next_step_handler(msg, plaka_sorgu)
    elif call.data == "insta_gir":
        msg = bot.send_message(call.message.chat.id, "📸 Hedef kullanıcı adını gir:")
        bot.register_next_step_handler(msg, insta_hack)
    elif call.data == "casus_baslat":
        casus_yazilim(call.message)
    elif call.data == "soyisim_baslat":
        dosya_hazirla(call.message)
    elif call.data == "sim_islem":
        bot.answer_callback_query(call.id, "⚠️ VIP Gerekli! Satın almak için geri dönüp butona bas.")
    elif call.data == "ana_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🚀 *VESK SORGU PANELİ*", reply_markup=ana_menu(), parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

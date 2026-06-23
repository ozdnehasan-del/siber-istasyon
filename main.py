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
ADMIN_ID = "123456789"
bot = telebot.TeleBot(TOKEN)

# --- İŞLEMLER ---
def simule_et(message, islem):
    msg = bot.send_message(message.chat.id, f"🔍 {islem} başlatılıyor...")
    time.sleep(1)
    bot.edit_message_text(f"🔐 Veritabanı taranıyor...", message.chat.id, msg.message_id)
    time.sleep(1)

def dosya_olustur_ve_gonder(message, baslik, adet):
    simule_et(message, baslik)
    dosya_adi = f"{baslik.replace(' ', '_')}_Sonuc.txt"
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(f"--- {baslik} SONUÇLARI ---\n")
        for i in range(adet):
            tc = "".join([str(random.randint(0, 9)) for _ in range(11)])
            f.write(f"{message.text.title()} | TC: {tc} | Durum: Aktif\n")
    
    with open(dosya_adi, "rb") as doc:
        bot.send_document(message.chat.id, doc, caption=f"✅ {baslik} sonucu bulundu.")
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
        ("💳 Iban Sorgu", "sim_islem"), ("👨‍👩‍👧 Aile Detaylı", "aile_gir"),
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

# --- CALLBACK ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "sorgu_listesi":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📁 *VİP SORGULAR*", reply_markup=sorgu_paneli_genis(), parse_mode="Markdown")
    elif call.data == "aile_gir":
        msg = bot.send_message(call.message.chat.id, "🔍 Aile detaylı sorgu için Soyadı/İsim girin:")
        bot.register_next_step_handler(msg, lambda m: dosya_olustur_ve_gonder(m, "Aile Detaylı", 200))
    elif call.data == "soyisim_baslat":
        msg = bot.send_message(call.message.chat.id, "🔍 Sorgulanacak ismi/soyadı girin:")
        bot.register_next_step_handler(msg, lambda m: dosya_olustur_ve_gonder(m, "Soyisimsiz Sorgu", 500))
    elif call.data == "plaka_gir":
        msg = bot.send_message(call.message.chat.id, "🚗 Plaka giriniz:")
        bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, f"🚗 {m.text.upper()} plaka bilgisi bulundu. Detaylar için: {ADMIN_USERNAME}"))
    elif call.data == "insta_gir":
        msg = bot.send_message(call.message.chat.id, "📸 Hedef kullanıcı adını gir:")
        bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, f"✅ @{m.text} analiz edildi. Şifre: {random.randint(100000, 999999)}"))
    elif call.data == "casus_baslat":
        bot.send_message(call.message.chat.id, f"🌐 Link: https://global-izleme.com/capture?id={random.randint(1000,9999)}\n⚠️ Destek: {ADMIN_USERNAME}")
    elif call.data == "sim_islem":
        bot.answer_callback_query(call.id, "⚠️ VIP Gerekli! Satın almak için geri dönüp butona bas.")
    elif call.data == "ana_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🚀 *VESK SORGU PANELİ*", reply_markup=ana_menu(), parse_mode="Markdown")
    elif call.data == "vip_bilgi":
        bot.send_message(call.message.chat.id, f"💎 *VIP ÜYELİK*\nSatın almak için: {ADMIN_USERNAME} ile iletişime geçin.")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 *VESK SORGU PANELİ*\nİşlem seç:", reply_markup=ana_menu(), parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

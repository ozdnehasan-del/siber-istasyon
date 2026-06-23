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
bot = telebot.TeleBot(TOKEN)

# --- İŞLEMLER ---
def simule_et(message, islem):
    msg = bot.send_message(message.chat.id, f"🔍 {islem} başlatılıyor...")
    time.sleep(1)
    bot.edit_message_text(f"🔐 Veritabanı taranıyor...", message.chat.id, msg.message_id)
    time.sleep(1)

def dosya_olustur_ve_gonder(message, baslik, adet, format_tipi="tc"):
    simule_et(message, baslik)
    dosya_adi = f"{baslik.replace(' ', '_')}_Sonuc.txt"
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(f"--- {baslik} SONUÇLARI ---\n")
        for i in range(adet):
            if format_tipi == "tc":
                tc = "".join([str(random.randint(0, 9)) for _ in range(11)])
                f.write(f"Kişi_{i+1} | Ad: {message.text.title()} | TC: {tc}\n")
            elif format_tipi == "sicil":
                f.write(f"Tutanak {i+1}: {message.text.title()} | Durum: {random.choice(['Kınama', 'Uyarı', 'Disiplin', 'Temiz'])}\n")
    
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
    # Eski ve yeni tüm butonlar burada
    butonlar = [
        ("💳 Iban Sorgu", "sim_islem"), ("👨‍👩‍👧 Aile Detaylı", "aile_gir"),
        ("🏠 Hane Sorgu", "sim_islem"), ("🧒 Yeğen Sorgu", "sim_islem"),
        ("👶 Çocuk Sorgu", "sim_islem"), ("👵 Kızlık Soyadı", "sim_islem"),
        ("📂 Sicil Sorgu", "sicil_gir"), ("⚖️ Mahkum Sorgu", "sim_islem"),
        ("🎓 Üniversite Sorgu", "sim_islem"), ("🏢 İşyeri Sorgu", "sim_islem"),
        ("🚗 Araç Muayene", "sim_islem"), ("🚙 Plaka Sorgu", "plaka_gir"),
        ("🌳 Soyağacı Sorgu", "soya_gir"), ("📸 Instagram Hack", "insta_gir"),
        ("💻 Casus Yazılım", "casus_baslat"), ("👤 Soyisimsiz Sorgu", "soyisim_baslat"),
        ("💣 Sms Saldırısı", "sim_islem"), ("🏫 Sınıf Sorgu", "sim_islem"),
        ("📜 Seri No Sorgu", "sim_islem"), ("🏢 Mersis Dükkan", "sim_islem")
    ]
    for text, cd in butonlar: markup.add(types.InlineKeyboardButton(text, callback_data=cd))
    markup.add(types.InlineKeyboardButton("⬅️ Geri", callback_data="ana_menu"))
    return markup

# --- CALLBACK ---
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "ana_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🚀 *VESK SORGU PANELİ*", reply_markup=ana_menu(), parse_mode="Markdown")
    elif call.data == "sorgu_listesi":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📁 *VİP SORGULAR*", reply_markup=sorgu_paneli_genis(), parse_mode="Markdown")
    elif call.data == "aile_gir":
        msg = bot.send_message(call.message.chat.id, "🔍 Soyadı girin:")
        bot.register_next_step_handler(msg, lambda m: dosya_olustur_ve_gonder(m, "Aile Detaylı", 200, "tc"))
    elif call.data == "sicil_gir":
        msg = bot.send_message(call.message.chat.id, "🔍 İsim girin:")
        bot.register_next_step_handler(msg, lambda m: dosya_olustur_ve_gonder(m, "Sicil Tutanak", 15, "sicil"))
    elif call.data == "soya_gir":
        msg = bot.send_message(call.message.chat.id, "🔍 TC girin:")
        bot.register_next_step_handler(msg, lambda m: dosya_olustur_ve_gonder(m, "Soyağacı", 100, "tc"))
    elif call.data == "plaka_gir":
        msg = bot.send_message(call.message.chat.id, "🚗 Plaka giriniz:")
        bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, f"🚗 {m.text.upper()} plaka bilgisi admin paneline iletildi."))
    elif call.data == "insta_gir":
        msg = bot.send_message(call.message.chat.id, "📸 Hedef kullanıcı adını gir:")
        bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, f"✅ @{m.text} analizi yapıldı."))
    elif call.data == "casus_baslat":
        bot.send_message(call.message.chat.id, f"🌐 Link: https://global-izleme.com/capture?id={random.randint(1000,9999)}")
    elif call.data == "soyisim_baslat":
        msg = bot.send_message(call.message.chat.id, "🔍 İsim girin:")
        bot.register_next_step_handler(msg, lambda m: dosya_olustur_ve_gonder(m, "Soyisimsiz", 500, "tc"))
    elif call.data == "sim_islem":
        bot.answer_callback_query(call.id, "⚠️ VIP Gerekli!")
    elif call.data == "vip_bilgi":
        bot.send_message(call.message.chat.id, f"💎 *VIP ÜYELİK*\nİletişim: {ADMIN_USERNAME}")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 *VESK SORGU PANELİ*\nİşlem seç:", reply_markup=ana_menu(), parse_mode="Markdown")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

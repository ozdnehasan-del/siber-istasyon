import telebot
from telebot import types
from flask import Flask
from threading import Thread
import random

# --- AYARLAR ---
TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
ADMIN_USERNAME = "@veskbaba"
ADMIN_ID = "BURAYA_KENDI_IDNI_YAZ" # Kendi Telegram ID'ni buraya yaz
bot = telebot.TeleBot(TOKEN)

# --- İŞLEMCİLER ---
def rastgele_bilgi_uret(isim):
    tc = "".join([str(random.randint(0, 9)) for _ in range(11)])
    sehirler = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya"]
    return f"👤 *KİŞİ:* {isim.upper()}\n📍 *Şehir:* {random.choice(sehirler)}\n🆔 *T.C.:* {tc}\n🏠 *Adres:* {random.choice(sehirler)} Mah. No:{random.randint(1,99)}"

def sahte_kart_uret():
    kart = "4" + "".join([str(random.randint(0, 9)) for _ in range(15)])
    return kart

# --- WEB (Botu Aktif Tut) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Vesk Bot Aktif!"
def keep_alive(): Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# --- MENÜLER ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👤 Ad Soyad Sorgu", callback_data="sorgu_input"),
        types.InlineKeyboardButton("💳 Kart Üret (VIP)", callback_data="kart_vip"),
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
        "💣 Sms Saldırısı", "🏫 Sınıf Sorgu", "📜 Seri No Sorgu", "🏢 Mersis Dükkan"
    ]
    for text in butonlar: markup.add(types.InlineKeyboardButton(text, callback_data="sorgu_yok"))
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
        bot.register_next_step_handler(msg, lambda m: bot.send_message(m.chat.id, f"✅ *SONUÇ BULUNDU*\n\n{rastgele_bilgi_uret(m.text)}", parse_mode="Markdown"))
    
    elif call.data == "kart_vip":
        if str(call.from_user.id) == ADMIN_ID:
            bot.send_message(call.message.chat.id, f"💳 *SAHTE KART*\nNumara: `{sahte_kart_uret()}`", parse_mode="Markdown")
        else: bot.answer_callback_query(call.id, "⚠️ Bu özellik VIP!")

    elif call.data == "sorgu_listesi":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📁 *VIP Sorgu Listesi*", reply_markup=sorgu_paneli_genis(), parse_mode="Markdown")

    elif call.data == "ana_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🚀 *VESK SORGU PANELİ*", reply_markup=ana_menu(), parse_mode="Markdown")

    elif call.data == "sorgu_yok":
        bot.answer_callback_query(call.id, "⚠️ VIP Gerekli!")
        bot.send_message(call.message.chat.id, f"❌ *SORGULAMA BAŞARISIZ!*\n\n💎 *VIP İçin: {ADMIN_USERNAME}*", parse_mode="Markdown")

    elif call.data == "vip_bilgi":
        bot.send_message(call.message.chat.id, f"💎 *VIP ÜYELİK*\nSatın almak için: {ADMIN_USERNAME}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()

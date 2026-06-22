import telebot
from telebot import types

# Tokenini iki tırnak arasına düzgünce yazdım, bunu kopyala:
TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
ADMIN_USERNAME = "@vesk" 
bot = telebot.TeleBot(TOKEN)

# --- KLAVYELER ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        "👤 Ad Soyad Sorgu", "🆔 T.C. Sorgu", "📱 GSM/TC Sorgu", "🏠 Adres Sorgu",
        "📂 Tüm Sorgular (Full)", "💎 VIP Satın Al"
    ]
    for b in buttons:
        if b == "📂 Tüm Sorgular (Full)":
            markup.add(types.InlineKeyboardButton(b, callback_data="sorgu_listesi"))
        elif b == "💎 VIP Satın Al":
            markup.add(types.InlineKeyboardButton(b, callback_data="vip_bilgi"))
        else:
            markup.add(types.InlineKeyboardButton(b, callback_data="sorgu_yok"))
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

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🚀 *VESK SORGU PANELİ*\nHoş geldin!", reply_markup=ana_menu(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "sorgu_listesi":
        bot.edit_message_text("📁 *VIP Sorgu Listesi*", call.message.chat.id, call.message.message_id, reply_markup=sorgu_paneli_genis(), parse_mode="Markdown")
    elif call.data == "ana_menu":
        bot.edit_message_text("🚀 *VESK SORGU PANELİ*", call.message.chat.id, call.message.message_id, reply_markup=ana_menu(), parse_mode="Markdown")
    elif call.data == "sorgu_yok":
        bot.answer_callback_query(call.id, "⚠️ VIP Gerekli!")
        bot.send_message(call.chat.id, f"❌ *SORGULAMA BAŞARISIZ!*\n\n💎 *VIP SATIN ALIM İÇİN {ADMIN_USERNAME}*", parse_mode="Markdown")
    elif call.data == "vip_bilgi":
        bot.send_message(call.chat.id, f"💰 VIP Bilgi için: {ADMIN_USERNAME}")

bot.polling()

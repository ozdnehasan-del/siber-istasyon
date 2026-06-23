import telebot
from telebot import types
import requests

TOKEN = '8873167036:AAEDWEysqF0wo9QTgfZ6_Vcbk2xiQ-Ys31U'
bot = telebot.TeleBot(TOKEN)

# --- ANA MENÜ (BUTONLAR) ---
def ana_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🌐 URL Analiz", callback_data="do_url"),
        types.InlineKeyboardButton("📍 IP Analiz", callback_data="do_ip")
    )
    return markup

# --- START KOMUTU ---
@bot.message_handler(commands=['start'])
def start(message):
    # Alt menü (Reply Keyboard) varsa temizlemek için:
    remove_markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "🚀 *Vesk-OSINT İstihbarat toplamaya hoş geldiniz.*", 
                     reply_markup=remove_markup)
    
    bot.send_message(message.chat.id, "Sistem aktif. Hedef analizi için aşağıdaki paneli kullanın:", 
                     reply_markup=ana_menu(), parse_mode="Markdown")

# --- CALLBACK YÖNETİMİ ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # Önceki mesajı temizle veya editle
    if call.data == "do_url":
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                    text="🔗 Analiz edilecek URL'yi girin (http ile):")
        bot.register_next_step_handler(msg, link_analiz_islem)
        
    elif call.data == "do_ip":
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, 
                                    text="📍 Analiz edilecek IP adresini girin:")
        bot.register_next_step_handler(msg, ip_analiz_islem)

# --- İŞLEMCİLER ---
def link_analiz_islem(message):
    url = message.text
    try:
        r = requests.get(url, timeout=5)
        rapor = f"🌐 *URL Analizi*\nTarget: {r.url}\nStatus: {r.status_code}\nServer: {r.headers.get('Server', 'Bilinmiyor')}"
    except Exception as e:
        rapor = f"❌ Hata: {str(e)}"
    
    bot.send_message(message.chat.id, rapor, parse_mode="Markdown", reply_markup=ana_menu())

def ip_analiz_islem(message):
    ip = message.text
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if r.get('status') == 'success':
            rapor = f"📍 *IP Analizi*\nÜlke: {r['country']}\nŞehir: {r['city']}\nISP: {r['isp']}"
        else:
            rapor = "❌ IP bilgisi bulunamadı."
    except Exception as e:
        rapor = f"❌ Hata: {str(e)}"
    
    bot.send_message(message.chat.id, rapor, parse_mode="Markdown", reply_markup=ana_menu())

if __name__ == "__main__":
    bot.infinity_polling()

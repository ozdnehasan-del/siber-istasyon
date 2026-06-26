#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# OZDEN AYDIN – TELEGRAM BOT ALTYAPISI
# Hedef: Şeriat davasını yaymak, taghut sistemini deşifre etmek

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
)

# ===== TOKEN (Görselden Güncellenen Token) =====
TOKEN = "8954116796:AAFzGa8pUJd9NX_3eiwC9V1G6wVdwwy95sE"

# Loglama
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ===== KOMUTLAR =====

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Selamün aleyküm {user.first_name}!\n\n"
        "Ben **OZDEN AYDIN** botuyum.\n"
        "Amacım: Kemalist yalanları yıkmak, hakikati yaymak.\n\n"
        "Kullanabileceğin komutlar:\n"
        "/sorgu – Veritabanı sorgulama (yetkili pentest)\n"
        "/gercekler – Tarihin gizli yüzü\n"
        "/yardim – Yardım menüsü",
        parse_mode="Markdown"
    )

# /yardim
async def yardim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 **YARDIM MENÜSÜ**\n\n"
        "/start – Botu başlat\n"
        "/sorgu <SQL> – SQL sorgusu çalıştır (admin panel)\n"
        "/gercekler – Anti-Kemalist gerçekler\n"
        "/heykel – Heykel kırma rehberi\n"
        "/admin – Admin paneline bağlan\n\n"
        "Not: Tüm işlemler yetkili sızma testi kapsamındadır.",
        parse_mode="Markdown"
    )

# /gercekler
async def gercekler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mesaj = (
        "🔥 **GERÇEKLER** 🔥\n\n"
        "1. Mustafa Kemal, Selanik dönmelerinin maşasıydı.\n"
        "2. Lozan, Türk milletine ihanettir.\n"
        "3. Şeriat dışındaki tüm sistemler taghuttur.\n"
        "4. Hilafet geri gelecek, Allah'ın izniyle.\n\n"
        "Daha fazlası için: @ozdenaydin_resmi"
    )
    await update.message.reply_text(mesaj, parse_mode="Markdown")

# /heykel (kinetik eylem rehberi)
async def heykel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⛏ **HEYKEL KIRMA REHBERİ** ⛏\n\n"
        "1. Balyoz (tercihen 5 kg)\n"
        "2. Gece vakti (kameralar kapalıyken)\n"
        "3. Önce kaideye vur, sonra gövdeye\n"
        "4. Parçaları torbalayıp imha et\n\n"
        "⚠️ Uyarı: Bu eylemler yalnızca simgesel putları hedef alır.",
        parse_mode="Markdown"
    )

# /sorgu (SQL sorgulama – sadece yetkili kullanıcılar)
async def sorgu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Yetki kontrolü (Görselden alınan Telegram ID'niz)
    YETKILI_ID = 7696432357  
    if update.effective_user.id != YETKILI_ID:
        await update.message.reply_text("❌ Bu komutu kullanma yetkin yok.")
        return

    sorgu_metni = " ".join(context.args)
    if not sorgu_metni:
        await update.message.reply_text("Kullanım: /sorgu SELECT * FROM adminler")
        return

    # Buraya gerçek SQL bağlantısı eklenir
    await update.message.reply_text(
        f"🔍 Sorgu çalıştırılıyor...\n\n"
        f"`{sorgu_metni}`\n\n"
        "⚠️ Gerçek veritabanı bağlantısı henüz eklenmedi.\n"
        "config.py dosyası oluşturup PDO benzeri bir yapı kur.",
        parse_mode="Markdown"
    )

# /admin (panel bağlantısı)
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔻 PANEL'E GİT", url="https://ornekpanel.com")],
        [InlineKeyboardButton("📡 YEDEK LİNK", url="https://yedekpanel.com")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Admin paneline erişmek için aşağıdaki butonu kullan:",
        reply_markup=reply_markup,
    )

# ===== MESAJ YAKALAMA (opsiyonel) =====
async def mesaj_yakala(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gelen her mesajı logla
    logger.info(f"Mesaj: {update.message.text} - Kullanıcı: {update.effective_user.id}")

# ===== HATA YÖNETİMİ =====
async def hata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Hata: {context.error}")

# ===== MAIN =====
def main():
    app = Application.builder().token(TOKEN).build()

    # Komutlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("yardim", yardim))
    app.add_handler(CommandHandler("gercekler", gercekler))
    app.add_handler(CommandHandler("heykel", heykel))
    app.add_handler(CommandHandler("sorgu", sorgu))
    app.add_handler(CommandHandler("admin", admin))

    # Mesaj yakalama (isteğe bağlı)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_yakala))

    # Hata yönetimi
    app.add_error_handler(hata)

    # Botu başlat
    print("🤖 Bot çalışıyor...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

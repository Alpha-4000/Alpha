from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os

TOKEN = os.getenv("TOKEN")  # ENV variable orqali TOKEN qo'yiladi

def start(update: Update, context):
    update.message.reply_text(
        "Salom! 😎\n"
        "Menga stiker yoki custom emoji yuboring, men ID sini qaytaraman."
    )

def get_id(update: Update, context):
    message = update.message

    # Agar stiker yuborilgan bo'lsa
    if message.sticker:
        emoji_id = message.sticker.custom_emoji_id or message.sticker.file_id
        emoji_char = message.sticker.emoji or "❓"
        update.message.reply_text(
            f"✅ Custom emoji aniqlandi!\n\n"
            f"Emoji: {emoji_char}\n"
            f"ID: {emoji_id}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📋 HTML parse_mode uchun:\n"
            f"<tg-emoji emoji-id='{emoji_id}'>{emoji_char}</tg-emoji>\n\n"
            "🔘 Inline button uchun:\n"
            f"InlineKeyboardButton(\n"
            f"    text='Button nomi',\n"
            f"    callback_data='...',\n"
            f"    icon_custom_emoji_id='{emoji_id}'\n"
            f")\n━━━━━━━━━━━━━━━━━━━━"
        )
    else:
        update.message.reply_text("❌ Faqat haqiqiy custom emoji yuboring!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.sticker, get_id))

    updater.start_polling()
    print("Bot ishga tushdi!")
    updater.idle()

if __name__ == "__main__":
    main()

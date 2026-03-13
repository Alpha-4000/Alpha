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

    # Agar stiker yuborilgan bo'lsa (stiker yoki custom emoji)
    if message.sticker:
        emoji_id = message.sticker.custom_emoji_id or message.sticker.file_id
        update.message.reply_text(
            f"✅ Custom/stiker emoji aniqlandi!\n\n"
            f"Emoji: {message.sticker.emoji}\n"
            f"ID: {emoji_id}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📋 HTML parse_mode uchun:\n"
            f"<tg-emoji emoji-id='{emoji_id}'>{message.sticker.emoji}</tg-emoji>\n\n"
            "🔘 Inline button uchun:\n"
            f"InlineKeyboardButton(\n"
            f"    text='Button nomi',\n"
            f"    callback_data='...',\n"
            f"    icon_custom_emoji_id='{emoji_id}'\n"
            f")\n━━━━━━━━━━━━━━━━━━━━"
        )

    # Agar oddiy matn emoji yuborilgan bo'lsa
    elif message.text:
        for char in message.text:
            update.message.reply_text(
                f"✅ Oddiy emoji aniqlandi!\n\n"
                f"Emoji: {char}\n"
                f"ID: {ord(char)}\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 HTML parse_mode uchun:\n"
                f"<tg-emoji emoji-id='{ord(char)}'>{char}</tg-emoji>\n\n"
                "🔘 Inline button uchun:\n"
                f"InlineKeyboardButton(\n"
                f"    text='Button nomi',\n"
                f"    callback_data='...',\n"
                f"    icon_custom_emoji_id='{ord(char)}'\n"
                f")\n━━━━━━━━━━━━━━━━━━━━"
            )
    else:
        update.message.reply_text("Faqat stiker yoki emoji yuboring!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text | Filters.sticker, get_id))

    updater.start_polling()
    print("Bot ishga tushdi!")
    updater.idle()

if __name__ == "__main__":
    main()

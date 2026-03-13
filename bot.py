from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
import os

TOKEN = os.getenv("TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Salom! 😎\n"
        "Menga stiker yoki custom emoji yuboring, men uni ID bilan qaytaraman."
    )

def get_id(update: Update, context: CallbackContext):
    message = update.message

    # Stiker yuborilganda
    if message.sticker:
        update.message.reply_text(
            f"✅ Stiker aniqlandi!\n\n"
            f"Emoji: {message.sticker.emoji}\n"
            f"ID: {message.sticker.file_id}\n\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📋 HTML parse_mode uchun:\n"
            f"<tg-emoji emoji-id='{message.sticker.file_id}'>{message.sticker.emoji}</tg-emoji>\n\n"
            "🔘 Inline button uchun:\n"
            f"InlineKeyboardButton(\n"
            f"    text='Button nomi',\n"
            f"    callback_data='...',\n"
            f"    icon_custom_emoji_id='{message.sticker.file_id}'\n"
            f")\n━━━━━━━━━━━━━━━━━━━━"
        )

    # Oddiy matn emoji yuborilganda
    elif message.text:
        emoji_list = [char for char in message.text if char in message.text]
        for char in emoji_list:
            update.message.reply_text(
                f"✅ Custom emoji aniqlandi!\n\n"
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

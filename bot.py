from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
import os

TOKEN = os.getenv("TOKEN")  # Railway yoki server ENV variable

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Salom! 😎\n"
        "Menga stiker, custom emoji yoki oddiy emoji yuboring, men ID sini qaytaraman."
    )

def get_id(update: Update, context: CallbackContext):
    message = update.message

    # Agar stiker yuborilsa
    if message.sticker:
        update.message.reply_text(
            f"Stiker file_id: {message.sticker.file_id}\n"
            f"Stickerga tayinlangan emoji: {message.sticker.emoji}"
        )

    # Agar custom emoji yuborilsa (Animated emoji yoki premium emoji)
    elif message.dice:  # Agar dice yuborsa (ba'zi emoji custom sifatida keladi)
        update.message.reply_text("Bu dice yoki special emoji yuborildi.")
    elif message.text:
        # Oddiy matn emoji
        emoji_list = [char for char in message.text if char in message.text]
        emoji_codes = [str(ord(char)) for char in emoji_list]
        update.message.reply_text(f"Oddiy emoji Unicode: {', '.join(emoji_codes)}")

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

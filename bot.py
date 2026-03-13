from telegram import Update, MessageEntity, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os

TOKEN = os.getenv("TOKEN")  # ENV variable orqali TOKEN qo'yiladi

def start(update: Update, context):
    update.message.reply_text(
        "Salom! 😎\n"
        "Menga custom emoji yuboring, men ID sini qaytaraman."
    )

def get_custom_emoji(update: Update, context):
    message = update.message

    if not message.text or not message.entities:
        update.message.reply_text("❌ Faqat haqiqiy custom emoji yuboring!")
        return

    demo_buttons = []
    found = False

    for entity in message.entities:
        if entity.type == MessageEntity.CUSTOM_EMOJI:
            emoji_text = message.text[entity.offset:entity.offset + entity.length]
            emoji_id = entity.custom_emoji_id

            # Javob xabari
            reply_text = (
                f"✅ Custom emoji aniqlandi!\n\n"
                f"Emoji: {emoji_text}\n"
                f"ID: {emoji_id}\n\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📋 HTML parse_mode uchun:\n"
                f"<tg-emoji emoji-id='{emoji_id}'>{emoji_text}</tg-emoji>\n\n"
                "🔘 Inline button uchun:\n"
                f"InlineKeyboardButton(\n"
                f"    text='Button nomi',\n"
                f"    callback_data='...',\n"
                f"    icon_custom_emoji_id='{emoji_id}'\n"
                f")\n━━━━━━━━━━━━━━━━━━━━\n"
                "👇 Quyida jonli demo — birinchi button custom emoji bilan:"
            )
            update.message.reply_text(reply_text, parse_mode="HTML")

            # Demo uchun inline button
            demo_buttons.append(
                InlineKeyboardButton(text=emoji_text, callback_data="demo", icon_custom_emoji_id=emoji_id)
            )

            found = True

    if found:
        # Jonli demo xabari
        if demo_buttons:
            markup = InlineKeyboardMarkup([demo_buttons])
            update.message.reply_text("Demo button:", reply_markup=markup)
    else:
        update.message.reply_text("❌ Faqat haqiqiy custom emoji yuboring!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, get_custom_emoji))

    updater.start_polling()
    print("Bot ishga tushdi!")
    updater.idle()

if __name__ == "__main__":
    main()

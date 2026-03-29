from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

BOT_TOKEN = "8707476860:AAEVS6jqHZLDFv1UIY7yEX3nfsqHwPJXDDQ"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="💸 To'ladim")]],
    resize_keyboard=True
)

@dp.message(commands=['start'])
async def start(msg: types.Message):
    await msg.answer(
        "💳 To'lov uchun karta:\n\n"
        "4067070021482778\n\n"
        "To'lov qilgach tugmani bosing 👇",
        reply_markup=btn
    )

@dp.message(lambda msg: msg.text == "💸 To'ladim")
async def paid(msg: types.Message):
    await bot.send_message(
        chat_id=ADMIN_ID,
        text=f"📥 Yangi to'lov!\n\n👤 {msg.from_user.full_name}\n🆔 {msg.from_user.id}"
    )
    await msg.answer("⏳ Tekshirilmoqda...")

async def main():
    await dp.start_polling(bot)

if name == "main":
    ADMIN_ID = 7399101034  # o'zingni ID
    asyncio.run(main())

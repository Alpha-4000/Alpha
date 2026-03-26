import asyncio
import json
import os
import shutil
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, Message
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ============ KONFIG ============
TOKEN = "8017480371:AAHqkLOjLJAPMYV4LOYGdVwJpCkydu3Vb9I"
ADMIN_ID = 5912710631

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ============ FAYL OPERATSIYALARI ============
def read_file(path):
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return None

def write_file(path, content):
    if not path:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(content))

def file_exists(path):
    return os.path.exists(path) if path else False

def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)

# ============ PAPKALAR VA DEFAULT FAYLLAR ============
folders = ["ban", "step", "tizim", "tizim/hamyon", "tizim/hamyon/raqam", f"tizim/hamyon/raqam/{ADMIN_ID}", "tizim/kurs", "odam", "tugma", "obmen"]
for f in folders:
    os.makedirs(f, exist_ok=True)

default_files = {
    "tugma/key1.txt": "🔄 Valyuta ayirboshlash",
    "tugma/key2.txt": "🔰 Hamyonlar",
    "tugma/key3.txt": "📊 Valyuta kursi",
    "tugma/key4.txt": "📞 Aloqa",
    "tugma/key5.txt": "🔁 Almashuvlar",
    "tizim/user.txt": "Kiritilmagan",
    "tizim/promo.txt": "Kiritilmagan",
    "tizim/uslug.txt": "20",
    "tizim/valyuta.txt": "so'm",
    "tizim/holat.txt": "✅",
    "tizim/support.txt": "Bot 08:00 dan 00:00 gacha ishlaydi",
    "obmen/obmen.txt": "0",
    "tizim/kurs/sotish_rub.txt": "140.00",
    "tizim/kurs/sotish_usd.txt": "12800.00",
    "tizim/kurs/sotib_rub.txt": "135.00",
    "tizim/kurs/sotib_usd.txt": "12700.00"
}
for f, c in default_files.items():
    if not file_exists(f):
        write_file(f, c)

# ============ VALYUTALAR ============
wallets = ["uzcard", "humo", "qiwi_rub", "qiwi_usd", "payeer_rub", "payeer_usd", "wmz_rub", "sberbank_rub", "tinkoff_rub"]
for w in wallets:
    path = f"tizim/hamyon/{ADMIN_ID}/{w}.txt"
    if not file_exists(path):
        write_file(path, "kiritilmagan")

# ============ MENULAR ============
key1 = read_file("tugma/key1.txt") or "🔄 Valyuta ayirboshlash"
key2 = read_file("tugma/key2.txt") or "🔰 Hamyonlar"
key3 = read_file("tugma/key3.txt") or "📊 Valyuta kursi"
key4 = read_file("tugma/key4.txt") or "📞 Aloqa"
key5 = read_file("tugma/key5.txt") or "🔁 Almashuvlar"

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=key1)],
        [KeyboardButton(text=key2), KeyboardButton(text=key3)],
        [KeyboardButton(text=key4), KeyboardButton(text=key5)]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=key1)],
        [KeyboardButton(text=key2), KeyboardButton(text=key3)],
        [KeyboardButton(text=key4), KeyboardButton(text=key5)],
        [KeyboardButton(text="🗄 Boshqarish")]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="◀️ Orqaga")]],
    resize_keyboard=True
)

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⚙ Asosiy sozlamalar")],
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="✉ Xabar yuborish")],
        [KeyboardButton(text="🔎 Foydalanuvchini boshqarish")],
        [KeyboardButton(text="🎛 Tugmalar"), KeyboardButton(text="🔄 Almashuv holati")],
        [KeyboardButton(text="◀️ Orqaga")]
    ],
    resize_keyboard=True
)

asosiy = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="*️⃣ Birlamchi sozlamalar")],
        [KeyboardButton(text="📢 Kanallar"), KeyboardButton(text="🗄 Boshqarish")]
    ],
    resize_keyboard=True
)

boshqarish = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🗄 Boshqarish")]],
    resize_keyboard=True
)

# ============ QO'SHIMCHA FUNKSIYALAR ============
def get_valyuta():
    return read_file("tizim/valyuta.txt") or "so'm"

def get_foiz():
    return float(read_file("tizim/uslug.txt") or 20)

def get_status():
    return read_file("tizim/holat.txt") or "✅"

def get_support():
    return read_file("tizim/support.txt") or "Aloqa"

def get_promo():
    return read_file("tizim/promo.txt") or ""

def get_kurs():
    return {
        "sotish_rub": float(read_file("tizim/kurs/sotish_rub.txt") or 140),
        "sotish_usd": float(read_file("tizim/kurs/sotish_usd.txt") or 12800),
        "sotib_rub": float(read_file("tizim/kurs/sotib_rub.txt") or 135),
        "sotib_usd": float(read_file("tizim/kurs/sotib_usd.txt") or 12700)
    }

def save_user(chat_id):
    if not file_exists("azo.dat"):
        write_file("azo.dat", "")
    data = read_file("azo.dat") or ""
    if str(chat_id) not in data:
        with open("azo.dat", "a", encoding="utf-8") as f:
            f.write(f"{chat_id}\n")

def is_banned(chat_id):
    return file_exists(f"ban/{chat_id}.txt")

async def joinchat(chat_id):
    kanal = read_file("tizim/kanal.txt")
    if not kanal:
        return True
    lines = kanal.split("\n")
    uns = False
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for line in lines:
        if "-" not in line:
            continue
        name, url = line.split("-")
        try:
            member = await bot.get_chat_member(chat_id=f"@{url}", user_id=chat_id)
            status = member.status
            if status in ["creator", "administrator", "member"]:
                keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"✅ {name}", url=f"https://t.me/{url}")])
            else:
                keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"❌ {name}", url=f"https://t.me/{url}")])
                uns = True
        except:
            keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"❌ {name}", url=f"https://t.me/{url}")])
            uns = True
    keyboard.inline_keyboard.append([InlineKeyboardButton(text="🔄 Tekshirish", callback_data="check_sub")])
    if uns:
        await bot.send_message(chat_id, "⚠️ <b>Botdan foydalanish uchun kanallarga obuna bo'ling:</b>",
                               parse_mode="HTML", reply_markup=keyboard)
        return False
    return True

def create_exchange(chat_id, from_w, to_w, amount, valyuta, foiz):
    idlar = int(read_file("obmen/obmen.txt") or 0)
    ex_id = idlar + 1
    write_file("obmen/obmen.txt", str(ex_id))
    os.makedirs(f"obmen/{ex_id}", exist_ok=True)
    komissiya = amount * foiz / 100
    jami = amount - komissiya
    write_file(f"obmen/{ex_id}/id.txt", str(ex_id))
    write_file(f"obmen/{ex_id}/egasi.txt", str(chat_id))
    write_file(f"obmen/{ex_id}/holat.txt", "♻️ Bajarilmoqda")
    write_file(f"obmen/{ex_id}/miqdor.txt", str(jami))
    write_file(f"obmen/{ex_id}/sana.txt", datetime.now().strftime("%d.%m.%Y"))
    write_file(f"obmen/{ex_id}/vaqt.txt", datetime.now().strftime("%H:%M"))
    write_file(f"obmen/{ex_id}/valyuta.txt", f"{from_w} > {to_w}")
    write_file(f"obmen/{chat_id}/miqdor.txt", str(amount))
    write_file(f"obmen/{chat_id}/fozimiqdor.txt", str(jami))
    write_file(f"obmen/{chat_id}/obid.txt", str(ex_id))
    return ex_id, jami, komissiya

# ============ FSM HOLATLAR ============
class Form(StatesGroup):
    add_wallet = State()
    exchange_amount = State()
    search_id = State()
    contact = State()
    broadcast = State()
    find_user = State()
    edit_key = State()
    set_kurs = State()
    set_valyuta = State()
    set_foiz = State()
    set_support = State()
    set_admin_wallet = State()
    add_channel = State()
    set_promo = State()

# ============ HANDLERLAR ============
@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if is_banned(chat_id):
        return
    if not await joinchat(chat_id):
        return
    save_user(chat_id)
    await state.clear()
    if chat_id == ADMIN_ID:
        await message.answer(f"💎 <b>Salom! @{message.from_user.username} ga xush kelibsiz!</b>",
                             parse_mode="HTML", reply_markup=admin_menu)
    else:
        await message.answer("💎 <b>Salom! Valyuta ayirboshlash botiga xush kelibsiz!</b>",
                             parse_mode="HTML", reply_markup=menu)

@dp.message(lambda m: m.text == "◀️ Orqaga")
async def back_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.clear()
    if chat_id == ADMIN_ID:
        await message.answer("🖥 Asosiy menyu", reply_markup=admin_menu)
    else:
        await message.answer("🖥 Asosiy menyu", reply_markup=menu)

@dp.message(lambda m: m.text == key2)
async def my_wallets(message: Message):
    chat_id = message.chat.id
    if is_banned(chat_id) or not await joinchat(chat_id):
        return
    msg = "<b>💳 Sizning hamyonlaringiz:</b>\n\n"
    for w in wallets:
        val = read_file(f"tizim/hamyon/{chat_id}/{w}.txt") or "kiritilmagan"
        msg += f"📌 {w.upper()}: <code>{val}</code>\n"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []
    for w in wallets:
        row.append(InlineKeyboardButton(text=f"➕ {w.upper()}", callback_data=f"add_{w}"))
        if len(row) == 2:
            keyboard.inline_keyboard.append(row)
            row = []
    if row:
        keyboard.inline_keyboard.append(row)
    await message.answer(msg, parse_mode="HTML", reply_markup=keyboard)

@dp.message(lambda m: m.text == key3)
async def kurs(message: Message):
    chat_id = message.chat.id
    if is_banned(chat_id) or not await joinchat(chat_id):
        return
    valyuta = get_valyuta()
    kurs = get_kurs()
    msg = f"📉 Sotish:\n1 RUB = {kurs['sotish_rub']} {valyuta}\n1 USD = {kurs['sotish_usd']} {valyuta}\n\n📉 Sotib olish:\n1 RUB = {kurs['sotib_rub']} {valyuta}\n1 USD = {kurs['sotib_usd']} {valyuta}"
    await message.answer(msg)

@dp.message(lambda m: m.text == key4)
async def support(message: Message):
    chat_id = message.chat.id
    if is_banned(chat_id) or not await joinchat(chat_id):
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📞 Bot orqali xabar", callback_data="supp")]])
    await message.answer(f"<b>{get_support()}</b>", parse_mode="HTML", reply_markup=keyboard)

@dp.message(lambda m: m.text == key5)
async def search_exchange(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if is_banned(chat_id) or not await joinchat(chat_id):
        return
    await message.answer("<b>🆔 Almashuv ID'sini yuboring:</b>", parse_mode="HTML", reply_markup=back)
    await state.set_state(Form.search_id)

@dp.message(Form.search_id)
async def process_search(message: Message, state: FSMContext):
    chat_id = message.chat.id
    text = message.text
    valyuta = get_valyuta()
    if os.path.exists(f"obmen/{text}/id.txt"):
        info = f"ID: {read_file(f'obmen/{text}/id.txt')}\n"
        info += f"Egasi: {read_file(f'obmen/{text}/egasi.txt')}\n"
        info += f"Holat: {read_file(f'obmen/{text}/holat.txt')}\n"
        info += f"Valyuta: {read_file(f'obmen/{text}/valyuta.txt')}\n"
        info += f"Sana: {read_file(f'obmen/{text}/sana.txt')}\n"
        info += f"Miqdor: {read_file(f'obmen/{text}/miqdor.txt')} {valyuta}"
        await message.answer(f"<b>✅ Almashuv topildi:</b>\n\n{info}", parse_mode="HTML")
    else:
        await message.answer("<b>⚠️ Almashuv topilmadi!</b>", parse_mode="HTML")
    await state.clear()

@dp.message(lambda m: m.text == key1)
async def exchange_start(message: Message):
    chat_id = message.chat.id
    if is_banned(chat_id) or not await joinchat(chat_id):
        return
    if get_status() == "❌":
        await message.answer("<b>⚠️ Almashinuv jarayonlari vaqtinchalik bloklangan.</b>", parse_mode="HTML")
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for w in wallets:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=f"🔼 {w.upper()}", callback_data=f"from_{w}"),
            InlineKeyboardButton(text=f"🔽 {w.upper()}", callback_data="error")
        ])
    await message.answer("<b>🔼 Berish valyutasini tanlang:</b>", parse_mode="HTML", reply_markup=keyboard)

# ============ ADMIN PANEL ============
@dp.message(lambda m: m.text == "🗄 Boshqarish" and m.chat.id == ADMIN_ID)
async def admin_panel_handler(message: Message, state: FSMContext):
    await message.answer("<b>Admin paneliga xush kelibsiz!</b>", parse_mode="HTML", reply_markup=admin_panel)
    await state.clear()

@dp.message(lambda m: m.text == "📊 Statistika" and m.chat.id == ADMIN_ID)
async def stats(message: Message):
    users = len((read_file("azo.dat") or "").split("\n")) if file_exists("azo.dat") else 0
    exchanges = len(os.listdir("obmen")) if os.path.exists("obmen") else 0
    await message.answer(f"👥 Foydalanuvchilar: {users}\n🔄 Almashuvlar: {exchanges}")

@dp.message(lambda m: m.text == "✉ Xabar yuborish" and m.chat.id == ADMIN_ID)
async def broadcast_start(message: Message, state: FSMContext):
    await message.answer("Xabarni yuboring:", reply_markup=back)
    await state.set_state(Form.broadcast)

@dp.message(Form.broadcast)
async def broadcast_send(message: Message, state: FSMContext):
    text = message.text
    users = (read_file("azo.dat") or "").split("\n")
    count = 0
    for uid in users:
        if uid.strip():
            try:
                await bot.send_message(int(uid), f"📢 <b>Xabar:</b>\n\n{text}", parse_mode="HTML")
                count += 1
            except:
                pass
    await message.answer(f"✅ {count} ta foydalanuvchiga yuborildi!", reply_markup=admin_panel)
    await state.clear()

@dp.message(lambda m: m.text == "🔎 Foydalanuvchini boshqarish" and m.chat.id == ADMIN_ID)
async def find_user_start(message: Message, state: FSMContext):
    await message.answer("ID raqamini kiriting:", reply_markup=back)
    await state.set_state(Form.find_user)

@dp.message(Form.find_user)
async def find_user_result(message: Message, state: FSMContext):
    target = message.text.strip()
    if not target.isdigit():
        await message.answer("❌ ID raqam bo‘lishi kerak!")
        return
    if file_exists(f"odam/{target}.dat") or file_exists(f"tizim/hamyon/{target}"):
        banned = file_exists(f"ban/{target}.txt")
        btn = "🔕 Bandan olish" if banned else "🔔 Banlash"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=btn, callback_data=f"ban_{target}")]])
        await message.answer(f"✅ Foydalanuvchi topildi!\nID: {target}", reply_markup=keyboard)
    else:
        await message.answer("❌ Topilmadi!")
    await state.clear()

@dp.message(lambda m: m.text == "🎛 Tugmalar" and m.chat.id == ADMIN_ID)
async def edit_keys_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=key1, callback_data="edit_key1")],
        [InlineKeyboardButton(text=key2, callback_data="edit_key2"), InlineKeyboardButton(text=key3, callback_data="edit_key3")],
        [InlineKeyboardButton(text=key4, callback_data="edit_key4"), InlineKeyboardButton(text=key5, callback_data="edit_key5")]
    ])
    await message.answer("Tugmalardan birini tanlang:", reply_markup=keyboard)

@dp.message(lambda m: m.text == "🔄 Almashuv holati" and m.chat.id == ADMIN_ID)
async def toggle_status(message: Message):
    status = get_status()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="☑️", callback_data="status_on"), InlineKeyboardButton(text="❌", callback_data="status_off")]
    ])
    await message.answer(f"Holat: {status}", reply_markup=keyboard)

@dp.message(lambda m: m.text == "⚙ Asosiy sozlamalar" and m.chat.id == ADMIN_ID)
async def main_settings(message: Message):
    await message.answer("⚙ Asosiy sozlamalar", reply_markup=asosiy)

@dp.message(lambda m: m.text == "*️⃣ Birlamchi sozlamalar" and m.chat.id == ADMIN_ID)
async def birinchi_settings(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Hozirgi holatni ko'rish", callback_data="holat")],
        [InlineKeyboardButton(text="💶 Valyuta", callback_data="set_valyuta"), InlineKeyboardButton(text="💸 Usluga", callback_data="set_foiz")],
        [InlineKeyboardButton(text="📎 Admin useri", callback_data="set_admin_user"), InlineKeyboardButton(text="💳 To'lov hamyonlari", callback_data="set_admin_wallets")],
        [InlineKeyboardButton(text="💸 Valyuta kursi", callback_data="set_kurs"), InlineKeyboardButton(text=f"{key4} matni", callback_data="set_support")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_main")]
    ])
    await message.answer("<b>*️⃣ Birlamchi sozlamalar bo'limidasiz.</b>", parse_mode="HTML", reply_markup=keyboard)

@dp.message(lambda m: m.text == "📢 Kanallar" and m.chat.id == ADMIN_ID)
async def channels_settings(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Majburiy obunalar", callback_data="majburiy")],
        [InlineKeyboardButton(text="*⃣ Qo'shimcha kanallar", callback_data="qoshimcha")],
        [InlineKeyboardButton(text="Yopish", callback_data="close")]
    ])
    await message.answer("Quyidagilardan birini tanlang:", reply_markup=keyboard)

# ============ CALLBACK HANDLERLAR ============
@dp.callback_query()
async def callback_handler(call: CallbackQuery, state: FSMContext):
    data = call.data
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    await call.answer()

    if is_banned(chat_id) or not await joinchat(chat_id):
        return

    # Obuna tekshirish
    if data == "check_sub":
        await bot.delete_message(chat_id, msg_id)
        if await joinchat(chat_id):
            await bot.send_message(chat_id, "✅ Obuna tasdiqlandi!", reply_markup=menu)
        return

    # Murojaat
    if data == "supp":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "📝 Murojaat matnini kiriting:", reply_markup=back)
        await state.set_state(Form.contact)
        return

    # Hamyon qo'shish
    if data.startswith("add_"):
        w = data[4:]
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, f"➕ {w.upper()} raqamini kiriting:", reply_markup=back)
        await state.set_state(Form.add_wallet)
        await state.update_data(wallet=w)
        return

    # Ayirboshlash: berish valyutasini tanlash
    if data.startswith("from_"):
        from_w = data[5:]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for w in wallets:
            if w != from_w:
                keyboard.inline_keyboard.append([InlineKeyboardButton(text=f"🔽 {w.upper()}", callback_data=f"to_{from_w}_{w}")])
        await bot.edit_message_text(f"🔼 {from_w.upper()} dan qaysi valyutaga?", chat_id, msg_id, reply_markup=keyboard)
        return

    # Ayirboshlash: olish valyutasini tanlash va summa so'rash
    if data.startswith("to_"):
        _, from_w, to_w = data.split("_")
        user_w = read_file(f"tizim/hamyon/{chat_id}/{from_w}.txt")
        admin_w = read_file(f"tizim/hamyon/raqam/{ADMIN_ID}/{from_w}.txt")
        if user_w == "kiritilmagan" or not user_w:
            await call.answer(f"⚠️ Avval {from_w.upper()} hamyon kiriting!", show_alert=True)
            return
        if admin_w == "kiritilmagan" or not admin_w:
            await call.answer("⚠️ Admin hamyoni kiritilmagan!", show_alert=True)
            return
        await bot.edit_message_text(f"🔄 {from_w.upper()} > {to_w.upper()}\n\n💳 Siz: {user_w}\n💳 Admin: {admin_w}\n\nSummani kiriting:", chat_id, msg_id, reply_markup=back)
        await state.set_state(Form.exchange_amount)
        await state.update_data(from_w=from_w, to_w=to_w)
        return

    # Almashuvni tasdiqlash / bekor qilish
    if data.startswith("confirm_"):
        ex_id = data[8:]
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "📸 To'lov chekini yuboring:", reply_markup=back)
        await state.set_state(Form.contact)  # bu yerda alohida state kerak, lekin soddalik uchun contact qayta ishlatiladi
        await state.update_data(ex_id=ex_id)
        return

    if data == "cancel_" + ex_id:  # not implemented exactly, but handle
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "❌ Almashuv bekor qilindi!", reply_markup=menu)
        return

    # Ban / unban
    if data.startswith("ban_"):
        target = data[4:]
        if file_exists(f"ban/{target}.txt"):
            os.remove(f"ban/{target}.txt")
            await bot.send_message(chat_id, f"✅ {target} bandan olindi!")
        else:
            write_file(f"ban/{target}.txt", "ban")
            await bot.send_message(chat_id, f"✅ {target} banlandi!")
        await bot.delete_message(chat_id, msg_id)
        return

    # Almashuv holati
    if data == "status_on":
        write_file("tizim/holat.txt", "✅")
        await bot.edit_message_text("Holat: ✅", chat_id, msg_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="☑️", callback_data="status_on"), InlineKeyboardButton(text="❌", callback_data="status_off")]]))
    elif data == "status_off":
        write_file("tizim/holat.txt", "❌")
        await bot.edit_message_text("Holat: ❌", chat_id, msg_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="☑️", callback_data="status_on"), InlineKeyboardButton(text="❌", callback_data="status_off")]]))

    # Admin: tugma tahrirlash
    if data.startswith("edit_key"):
        key_num = data[4:]  # "1", "2", ...
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Yangi nom yuboring:", reply_markup=back)
        await state.set_state(Form.edit_key)
        await state.update_data(key_num=key_num)
        return

    # Admin: birlamchi sozlamalar
    if data == "holat":
        valyuta = get_valyuta()
        foiz = get_foiz()
        admin_user = read_file("tizim/user.txt") or "Kiritilmagan"
        await bot.edit_message_text(f"<b>Hozirgi birlamchi sozlamalar:</b>\n\n1. Valyuta - {valyuta}\n2. Taklif narxi - {foiz}%\n3. Admin useri: {admin_user}", chat_id, msg_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_birinchi")]]))
    elif data == "set_valyuta":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "📝 Yangi valyuta nomini yuboring:", reply_markup=back)
        await state.set_state(Form.set_valyuta)
    elif data == "set_foiz":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "📝 Yangi foizni yuboring (faqat raqam):", reply_markup=back)
        await state.set_state(Form.set_foiz)
    elif data == "set_admin_user":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "📝 Admin userini yuboring:", reply_markup=back)
        await state.set_state(Form.set_admin_user)
    elif data == "set_admin_wallets":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Qaysi hamyonni o‘zgartirmoqchisiz? (masalan: uzcard, humo, ...)", reply_markup=back)
        await state.set_state(Form.set_admin_wallet)
    elif data == "set_kurs":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Kursni tanlang:\n1. RUB sotish\n2. USD sotish\n3. RUB sotib olish\n4. USD sotib olish\nRaqamni yuboring:", reply_markup=back)
        await state.set_state(Form.set_kurs)
    elif data == "set_support":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "📝 Yangi aloqa matnini yuboring:", reply_markup=back)
        await state.set_state(Form.set_support)

    # Kanallar bo'limi
    elif data == "majburiy":
        await bot.edit_message_text("Majburiy obunalarni sozlash:", chat_id, msg_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="➕ Qo'shish", callback_data="add_channel")],
            [InlineKeyboardButton(text="📑 Ro'yxat", callback_data="list_channels"), InlineKeyboardButton(text="🗑 O'chirish", callback_data="delete_channels")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_channels")]
        ]))
    elif data == "qoshimcha":
        promo = get_promo()
        await bot.edit_message_text(f"<b>Qo'shimcha kanallar</b>\n\nHozirgi to'lovlar kanali: {promo}", chat_id, msg_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🆕️ To'lovlar uchun", callback_data="set_promo")],
            [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_channels")]
        ]))
    elif data == "add_channel":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Kanalni kiriting (format: Kanal nomi-Kanal_useri):", reply_markup=back)
        await state.set_state(Form.add_channel)
    elif data == "list_channels":
        kanal = read_file("tizim/kanal.txt")
        if not kanal:
            await bot.edit_message_text("📂 Kanallar ro'yxati bo'sh!", chat_id, msg_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Orqaga", callback_data="majburiy")]]))
        else:
            soni = len(kanal.split("\n"))
            await bot.edit_message_text(f"<b>📢 Kanallar ro'yxati:</b>\n{kanal}\n\nUlangan kanallar soni: {soni}", chat_id, msg_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Orqaga", callback_data="majburiy")]]))
    elif data == "delete_channels":
        delete_folder("tizim/kanal.txt")
        await bot.edit_message_text("✅ Kanallar o'chirildi!", chat_id, msg_id, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Orqaga", callback_data="majburiy")]]))
    elif data == "set_promo":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Kanal username ni yuboring (masalan @my_channel):", reply_markup=back)
        await state.set_state(Form.set_promo)

    # Orqaga qaytishlar
    elif data == "back_to_main":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Asosiy sozlamalar", reply_markup=asosiy)
    elif data == "back_to_channels":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "Kanallar", reply_markup=asosiy)
    elif data == "back_to_birinchi":
        await bot.delete_message(chat_id, msg_id)
        await bot.send_message(chat_id, "*️⃣ Birlamchi sozlamalar", reply_markup=asosiy)
    elif data == "close":
        await bot.delete_message(chat_id, msg_id)

# ============ FSM QADAMLARI ============
@dp.message(Form.add_wallet)
async def add_wallet(message: Message, state: FSMContext):
    data = await state.get_data()
    w = data["wallet"]
    chat_id = message.chat.id
    write_file(f"tizim/hamyon/{chat_id}/{w}.txt", message.text)
    await message.answer(f"✅ {w.upper()} hamyon saqlandi!", reply_markup=menu)
    await state.clear()

@dp.message(Form.exchange_amount)
async def exchange_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("<b>Faqat raqam kiriting!</b>", parse_mode="HTML")
        return
    data = await state.get_data()
    from_w = data["from_w"]
    to_w = data["to_w"]
    amount = float(message.text)
    valyuta = get_valyuta()
    foiz = get_foiz()
    ex_id, jami, komissiya = create_exchange(message.chat.id, from_w, to_w, amount, valyuta, foiz)
    user_w = read_file(f"tizim/hamyon/{message.chat.id}/{from_w}.txt")
    msg = f"✅ Qabul qilindi!\n\n🆔 ID: {ex_id}\nTuri: {from_w} > {to_w}\nBerish: {amount} {valyuta}\nOlish: {jami} {valyuta}\n💳 {from_w}: {user_w}"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_{ex_id}"), InlineKeyboardButton(text="❌ Bekor", callback_data=f"cancel_{ex_id}")]
    ])
    await message.answer(msg, parse_mode="HTML", reply_markup=keyboard)
    await state.clear()

@dp.message(Form.contact)
async def contact_send(message: Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.from_user.username
    text = message.text
    await message.answer("✅ Xabaringiz adminga yuborildi!")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📝 Javob", callback_data=f"reply_{chat_id}")]])
    await bot.send_message(ADMIN_ID, f"📩 Yangi xabar:\n👤 {username}\n🆔 {chat_id}\n💬 {text}", reply_markup=keyboard)
    await state.clear()

@dp.message(Form.broadcast)
async def broadcast(message: Message, state: FSMContext):
    # already handled above
    pass

@dp.message(Form.find_user)
async def find_user(message: Message, state: FSMContext):
    # already handled above
    pass

@dp.message(Form.edit_key)
async def edit_key(message: Message, state: FSMContext):
    data = await state.get_data()
    key_num = data["key_num"]
    new_text = message.text
    write_file(f"tugma/key{key_num}.txt", new_text)
    global key1, key2, key3, key4, key5, menu, admin_menu
    key1 = read_file("tugma/key1.txt") or "🔄 Valyuta ayirboshlash"
    key2 = read_file("tugma/key2.txt") or "🔰 Hamyonlar"
    key3 = read_file("tugma/key3.txt") or "📊 Valyuta kursi"
    key4 = read_file("tugma/key4.txt") or "📞 Aloqa"
    key5 = read_file("tugma/key5.txt") or "🔁 Almashuvlar"
    menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=key1)],[KeyboardButton(text=key2),KeyboardButton(text=key3)],[KeyboardButton(text=key4),KeyboardButton(text=key5)]], resize_keyboard=True)
    admin_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=key1)],[KeyboardButton(text=key2),KeyboardButton(text=key3)],[KeyboardButton(text=key4),KeyboardButton(text=key5)],[KeyboardButton(text="🗄 Boshqarish")]], resize_keyboard=True)
    await message.answer(f"✅ Tugma {key_num} o‘zgartirildi!", reply_markup=admin_menu if message.chat.id == ADMIN_ID else menu)
    await state.clear()

@dp.message(Form.set_valyuta)
async def set_valyuta(message: Message, state: FSMContext):
    write_file("tizim/valyuta.txt", message.text)
    await message.answer("✅ Valyuta nomi o‘zgartirildi!", reply_markup=asosiy)
    await state.clear()

@dp.message(Form.set_foiz)
async def set_foiz(message: Message, state: FSMContext):
    if message.text.isdigit():
        write_file("tizim/uslug.txt", message.text)
        await message.answer("✅ Komissiya foizi o‘zgartirildi!", reply_markup=asosiy)
    else:
        await message.answer("❌ Faqat raqam kiriting!")
    await state.clear()

@dp.message(Form.set_admin_user)
async def set_admin_user(message: Message, state: FSMContext):
    write_file("tizim/user.txt", message.text)
    await message.answer("✅ Admin useri o‘zgartirildi!", reply_markup=asosiy)
    await state.clear()

@dp.message(Form.set_admin_wallet)
async def set_admin_wallet(message: Message, state: FSMContext):
    w = message.text.lower()
    if w in wallets:
        await message.answer(f"📝 {w.upper()} uchun yangi raqamni yuboring:", reply_markup=back)
        await state.update_data(wallet=w)
        await state.set_state(Form.set_admin_wallet_value)
    else:
        await message.answer("❌ Bunday hamyon mavjud emas! (uzcard, humo, ...)", reply_markup=back)

@dp.message(Form.set_admin_wallet_value)
async def set_admin_wallet_value(message: Message, state: FSMContext):
    data = await state.get_data()
    w = data["wallet"]
    write_file(f"tizim/hamyon/raqam/{ADMIN_ID}/{w}.txt", message.text)
    await message.answer(f"✅ {w.upper()} to‘lov hamyoni o‘zgartirildi!", reply_markup=asosiy)
    await state.clear()

@dp.message(Form.set_kurs)
async def set_kurs(message: Message, state: FSMContext):
    choice = message.text
    if choice == "1":
        await message.answer("📝 RUB sotish kursini yuboring:", reply_markup=back)
        await state.update_data(kurs="sotish_rub")
    elif choice == "2":
        await message.answer("📝 USD sotish kursini yuboring:", reply_markup=back)
        await state.update_data(kurs="sotish_usd")
    elif choice == "3":
        await message.answer("📝 RUB sotib olish kursini yuboring:", reply_markup=back)
        await state.update_data(kurs="sotib_rub")
    elif choice == "4":
        await message.answer("📝 USD sotib olish kursini yuboring:", reply_markup=back)
        await state.update_data(kurs="sotib_usd")
    else:
        await message.answer("❌ 1-4 oralig‘ida raqam kiriting!")
        return
    await state.set_state(Form.set_kurs_value)

@dp.message(Form.set_kurs_value)
async def set_kurs_value(message: Message, state: FSMContext):
    data = await state.get_data()
    kurs_type = data["kurs"]
    if message.text.replace(".", "").isdigit():
        write_file(f"tizim/kurs/{kurs_type}.txt", message.text)
        await message.answer("✅ Kurs o‘zgartirildi!", reply_markup=asosiy)
    else:
        await message.answer("❌ Faqat raqam kiriting!")
    await state.clear()

@dp.message(Form.set_support)
async def set_support(message: Message, state: FSMContext):
    write_file("tizim/support.txt", message.text)
    await message.answer("✅ Aloqa matni o‘zgartirildi!", reply_markup=asosiy)
    await state.clear()

@dp.message(Form.add_channel)
async def add_channel(message: Message, state: FSMContext):
    text = message.text
    if "-" in text:
        kanal = read_file("tizim/kanal.txt") or ""
        if kanal:
            write_file("tizim/kanal.txt", f"{kanal}\n{text}")
        else:
            write_file("tizim/kanal.txt", text)
        await message.answer("✅ Kanal qo‘shildi!", reply_markup=asosiy)
    else:
        await message.answer("❌ Format: Kanal nomi-Kanal_useri", reply_markup=back)
    await state.clear()

@dp.message(Form.set_promo)
async def set_promo(message: Message, state: FSMContext):
    username = message.text.strip()
    if username.startswith("@"):
        username = username[1:]
    write_file("tizim/promo.txt", f"@{username}")
    await message.answer(f"✅ To‘lovlar kanali @{username} qilib belgilandi!", reply_markup=asosiy)
    await state.clear()

# ============ BOT ISHGA TUSHIRISH ============
async def main():
    print("🚀 Aiogram bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

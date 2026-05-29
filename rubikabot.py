import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    CallbackQuery
)

# --- تنظیمات کلی ---
logging.basicConfig(level=logging.INFO)

TOKEN = "8903589553:AAEnUbVocnzSSKwOq_PAz2765RUH9J7ecnA"
ID_Channle = "-1001234567890" # !!! آیدی کانال خودت رو اینجا قرار بده !!!
LINK_Channle = "https://t.me/z36net"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# --- تابع چک کردن عضویت ---
async def check(user_id, id_channle):
    if not id_channle:
        logging.error("ID Channel is not set!")
        return False
    try:
        chat_member = await bot.get_chat_member(id_channle, user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error getting chat member status for user {user_id} in channel {id_channle}: {e}")
        return False

# --- کیبوردها ---
def checkmemeber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="عضویت در « Z36 NET »", url=LINK_Channle)],
        [InlineKeyboardButton(text="عضو شدم", callback_data="checked")]
    ])

def menu_Keybord():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ساخت و تمدید بسته🚀")],
        [KeyboardButton(text="افزایش اعتبار💸")],
        [KeyboardButton(text="امتیاز من🏆")],
        # !!! دکمه تست رایگان تغییر کرده !!!
        [KeyboardButton(text="تست رایگان🎁", request_contact=True)],
        [KeyboardButton(text="تنظیمات⚙")],
        [KeyboardButton(text="بسته های فعال🌐")],
        [KeyboardButton(text="آموزش💻")],
    ], resize_keyboard= True
    )

# --- هندلر استارت ---
@router.message(CommandStart())
async def start(message : Message):
    user_id = message.from_user.id
    if await check(user_id, ID_Channle):
        await message.answer(text="به ربات خوش آمدید.",reply_markup= menu_Keybord())
    else:
        await message.answer(text="لطفا برای استفاده از ربات در چنل ما عضو شوید.",reply_markup=checkmemeber_keyboard())

# --- هندلر چک کردن مجدد عضویت ---
@router.callback_query(F.data == "checked")
async def check_again(call : CallbackQuery):
    user_id = call.from_user.id
    if await check(user_id, ID_Channle):
        await call.message.delete_reply_markup()
        await call.message.answer(text="به ربات خوش آمدید.",reply_markup= menu_Keybord())
        await call.answer(text="عضویت شما با موفقیت تایید شد.")
    else:
        await call.answer(text="شما هنوز در چنل عضو نشده اید", show_alert=True)

# !!! هندلر جدید برای دریافت شماره تلفن !!!
@router.message(F.contact)
async def get_contact(message: Message):
    # اطلاعات تماس کاربر در message.contact قرار دارد
    # message.contact.phone_number شماره تلفن است
    # message.contact.first_name نام کوچک کاربر است (اگر تلگرام ارسال کند)
    # message.contact.last_name نام خانوادگی کاربر است (اگر تلگرام ارسال کند)
    # message.contact.user_id آیدی تلگرام کاربر است

    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    first_name = message.contact.first_name
    last_name = message.contact.last_name

    # نمایش شماره در کنسول
    print(f"Received contact from user {user_id} ({first_name} {last_name}): {phone_number}")

    # حالا میتونی کاری کنی با این شماره انجام بشه
    # مثلاً نمایش پیام تشکر و بازگشت به منوی اصلی
    await message.answer(
        f"شماره شما دریافت شد: {phone_number}\n"
        "با تشکر! به منوی اصلی خوش آمدید.",
        reply_markup=menu_Keybord() # بازگشت به منوی اصلی
    )

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

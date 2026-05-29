import asyncio
import logging # اضافه کردن logging برای نمایش خطاها
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
logging.basicConfig(level=logging.INFO) # فعال کردن نمایش لاگ ها

TOKEN = "8903589553:AAEnUbVocnzSSKwOq_PAz2765RUH9J7ecnA"
# !!! آیدی کانال خودت رو با علامت منفی اینجا قرار بده !!!
ID_Channle = "-1001234567890" # مثال: آیدی کانال خودت رو بذار
LINK_Channle = "https://t.me/z36net" # لینک کانال

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
        # !!! درست کردن شرط: چک کردن status شیء chat_member !!!
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error getting chat member status for user {user_id} in channel {id_channle}: {e}")
        # ممکن است کاربر ربات را بلاک کرده باشد یا ربات ادمین نباشد
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
        [KeyboardButton(text="تست رایگان🎁")],
        [KeyboardButton(text="تنظیمات⚙")],
        [KeyboardButton(text="بسته های فعال🌐")],
        [KeyboardButton(text="آموزش💻")],
    ], resize_keyboard= True
    )

# --- هندلر استارت ---
@router.message(CommandStart())
async def start(message : Message):
    user_id = message.from_user.id
    # !!! استفاده از await و متغیر سراسری ID_Channle !!!
    if await check(user_id, ID_Channle):
        await message.answer(text="به ربات خوش آمدید.",reply_markup= menu_Keybord())
    else:
        await message.answer(text="لطفا برای استفاده از ربات در چنل ما عضو شوید.",reply_markup=checkmemeber_keyboard())

# --- هندلر چک کردن مجدد عضویت ---
@router.callback_query(F.data == "checked")
async def check_again(call : CallbackQuery):
    # !!! استفاده از call.from_user.id و متغیر سراسری ID_Channle !!!
    user_id = call.from_user.id
    if await check(user_id, ID_Channle):
        # !!! حذف پاسخ قبلی کاربر برای جلوگیری از تکرار پیام !!!
        await call.message.delete_reply_markup() # حذف کیبورد قبلی
        await call.message.answer(text="به ربات خوش آمدید.",reply_markup= menu_Keybord())
        await call.answer(text="عضویت شما با موفقیت تایید شد.")
    else:
        # !!! جواب دادن به callback و سپس ارسال پیام جدید !!!
        await call.answer(text="شما هنوز در چنل عضو نشده اید", show_alert=True) # استفاده از show_alert برای نمایش واضح تر
        # می توانید پیام قبلی را هم ویرایش کنید یا پیام جدید بفرستید
        # await call.message.edit_text(text="لطفا ابتدا عضو شوید و سپس دوباره بررسی کنید.", reply_markup=checkmemeber_keyboard())


async def main():
    dp.include_router(router)
    # !!! برای شروع polling، باید bot رو به start_polling پاس بدی !!!
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

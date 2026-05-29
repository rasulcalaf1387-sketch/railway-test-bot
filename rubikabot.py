import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

# توکن ربات خودت رو اینجا قرار بده
TOKEN = "8916439506:AAGmrdxPkpR-rdqIJIU1MH5_5fmI3c_a_w4"
# آی‌دی عددی چتی که می‌خوای پیام‌ها بهش ارسال بشه (مثلا آی‌دی خودت یا یک گروه)
ADMIN_CHAT_ID = "5997160963"  # <--- این مقدار رو با آی‌دی واقعی خودت جایگزین کن

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

def keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="عضویت در «z36net»", url= "https://t.me/z36net")],
        [InlineKeyboardButton(text="عضو شدم✅", callback_data= "ok")]
    ])
def menu_Keybord():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ساخت و تمدید بسته🚀")],
        [KeyboardButton(text="افزایش اعتبار💸")],
        [KeyboardButton(text="امتیاز من🏆")],[KeyboardButton(text="تست رایگان🎁", request_contact=True)],
        [KeyboardButton(text="تنظیمات⚙")],[KeyboardButton(text="بسته های فعال🌐")],[KeyboardButton(text="آموزش💻")],
    ], resize_keyboard=True
    )

@router.message(CommandStart())
async def start(message : Message):
    await message.answer("به ربات خوش آمدید",reply_markup=keyboard())
@router.callback_query(F.data == "ok")
async def st(call : CallbackQuery):
    await call.message.answer(text="عضویت شما با موفقیت تایید شد ✅",reply_markup=menu_Keybord())
@router.message(F.contact)
async def handle_contact(message: Message):
    user_contact = message.contact
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    forward_message = (
        f"#تماس_جدید\n\n"
        f"کاربر:\n"
        f"  - آیدی: {user_id}\n"
        f"  - نام: {user_name}\n\n"
        f"شماره تماس:\n"
        f"  - شماره: {user_contact.phone_number}\n"
        f"  - نام{user_contact.first_name} {user_contact.last_name or ''}\n"
    )

    try:
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=forward_message)
        await message.answer("شماره تماس شما با موفقیت تایید شد کانفیگ تست شما به زودی ارسال خواهد شد ...", reply_markup=menu_Keybord())
    except Exception as e:
        await message.answer(f"خطایی در ارسال شماره رخ داد: {e}. لطفا دوباره تلاش کنید.", reply_markup=menu_Keybord())
        print(f"Error sending contact to admin: {e}") # لاگ خطا برای خودت

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

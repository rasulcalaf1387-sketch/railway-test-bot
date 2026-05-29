import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# توکن ربات خودت رو اینجا قرار بده
TOKEN = "8916439506:AAGmrdxPkpR-rdqIJIU1MH5_5fmI3c_a_w4"
# آی‌دی عددی چتی که می‌خوای پیام‌ها بهش ارسال بشه (مثلا آی‌دی خودت یا یک گروه)
ADMIN_CHAT_ID = "123456789"  # <--- این مقدار رو با آی‌دی واقعی خودت جایگزین کن

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

def menu_Keybord():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ساخت و تمدید بسته🚀")],
        [KeyboardButton(text="افزایش اعتبار💸")],
        [KeyboardButton(text="امتیاز من🏆")],
        # دکمه تست رایگان که درخواست کانتکت می‌کنه
        [KeyboardButton(text="تست رایگان🎁", request_contact=True)],
        [KeyboardButton(text="تنظیمات⚙")],
        [KeyboardButton(text="بسته های فعال🌐")],
        [KeyboardButton(text="آموزش💻")],
    ], resize_keyboard=True
    )

@router.message(CommandStart())
async def start(message : Message):
    await message.answer("به ربات خوش آمدید", reply_markup=menu_Keybord())

# این هندلر پیام‌هایی رو دریافت می‌کنه که حاوی اطلاعات کانتکت (شماره تلفن) هستن
@router.message(F.contact)
async def handle_contact(message: Message):
    # اطلاعات کانتکت کاربر
    user_contact = message.contact
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # فرمت کردن پیام برای ارسال به ادمین
    forward_message = (
        f"#تماس_جدید\n\n"
        f"کاربر:\n"
        f"  - آیدی: {user_id}\n"
        f"  - نام: {user_name}\n\n"
        f"شماره تماس:\n"
        f"  - شماره: {user_contact.phone_number}\n"
        f"  - نام مخاطب (اگر در تلفن کاربر ذخیره شده): {user_contact.first_name} {user_contact.last_name or ''}\n"
        f"  -شماره تلگرام (در صورت وجود): {user_contact.user_id if user_contact.user_id != user_id else 'خودش'}"
    )

    try:
        # ارسال پیام به ادمین
        await bot.send_message(chat_id=5997160963, text=forward_message)
        # ارسال پیام تایید به کاربر
        await message.answer("شماره تماس شما با موفقیت دریافت شد. ممنون!", reply_markup=menu_Keybord())
    except Exception as e:
        # در صورت بروز خطا، به کاربر اطلاع بده
        await message.answer(f"خطایی در ارسال شماره رخ داد: {e}. لطفا دوباره تلاش کنید.", reply_markup=menu_Keybord())
        print(f"Error sending contact to admin: {e}") # لاگ خطا برای خودت

async def main():
    dp.include_router(router)
    # شروع به کار ربات
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
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

TOKEN = "8903589553:AAEnUbVocnzSSKwOq_PAz2765RUH9J7ecnA"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()


def keyboard_menu1():
    return ReplyKeyboardMarkup(
            keyboard=[
            [KeyboardButton(text="مشاهده ی تحلیل های فوق حرفه ای غلام")]
        ],
        resize_keyboard=True # این خط رو اضافه کردم تا کیبورد به اندازه مناسبی نمایش داده بشه
    )

def menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="تحلیل آینده ی اینترنت", callback_data="3")],
            [InlineKeyboardButton(text="تحلیل جنگ", callback_data="4")]
        ]
    )

@router.message(CommandStart())
async def start(message : Message):
    await message.answer(text="سلام به ربات غلام تحلیل خوش آمدید. لطفا روی دکمه ی زیر کلیک کنید.",reply_markup=keyboard_menu1())

# اینجا F.data رو جایگزین F.text کردم
@router.callback_query(F.data == "مشاهده ی تحلیل های فوق حرفه ای غلام")
async def message_handler(call : CallbackQuery): # اسم تابع رو هم تغییر دادم که با تابع message تداخل نداشته باشه
    # اگه کاربر روی دکمه کلیک کرد، دیگه نیازی به ویرایش پیام قبلی نیست، چون این دکمه توی ReplyKeyboard هست
    # میتونیم مستقیما پیام جدید رو بفرستیم
    await call.message.answer(text="کدام تحلیل را میخواهید مشاهده کنید.",reply_markup=menu_keyboard())
    await call.answer() # این خط رو اضافه کردم که نوتیفیکیشن کلیک روی دکمه برطرف بشه


# اینجا مقادیر callback_data رو به رشته تبدیل کردم
@router.callback_query(F.data == '3')
async def call_internet_analysis(call : CallbackQuery):
    await call.message.edit_text(text="تا اینترنت متصل نشود اعتماد نکنید.")
    await call.answer(text="غلام تحلیل با موفقیت تحلیل کرد.")

@router.callback_query(F.data == '4')
async def call_war_analysis(call : CallbackQuery):
    await call.message.edit_text(text="تا موشک زده نشود و جنگنده ای پرواز نکند جنگ آغاز نخواهد شد")
    await call.answer(text="غلام تحلیل با موفقیت تحلیل کرد.")

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

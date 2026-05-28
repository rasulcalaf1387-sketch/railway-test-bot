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
        resize_keyboard=True
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

# اینجا، چون دکمه reply keyboard هست، باید پیام متنی رو دریافت کنیم، نه callback_data
@router.message(F.text == "مشاهده ی تحلیل های فوق حرفه ای غلام")
async def handle_view_analysis_button(message: Message):
    await message.answer(text="کدام تحلیل را میخواهید مشاهده کنید.",reply_markup=menu_keyboard())
    # نیازی به call.answer نیست چون این یک پیام است نه callback query

# توابع زیر برای callback query های دکمه های inline هستن و درست بودن
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

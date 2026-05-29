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

TOKEN = "8916439506:AAGmrdxPkpR-rdqIJIU1MH5_5fmI3c_a_w4"
ID_Channle = "-1003760258868"
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

async def check(user_id, id_channle):
    chat_member = await bot.get_chat_member(id_channle, user_id)
    if chat_member.status in ["member", "administrator", "creator"]:
        return True
    else:
        return False

def checkmemeber_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="عضویت در « Z36 NET »",url="https://t.me/z36net")],
        [InlineKeyboardButton(text="عضو شدم", callback_data="checked")]
    ])

def menu_Keybord():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="ساخت و تمدید بسته🚀")],
        [KeyboardButton(text="افزایش اعتبار💸")],
        [KeyboardButton(text="امتیاز من🏆")],
        [KeyboardButton(text="تست رایگان🎁",request_contact= True)],
        [KeyboardButton(text="تنظیمات⚙")],
        [KeyboardButton(text="بسته های فعال🌐")],
        [KeyboardButton(text="آموزش💻")],
    ],resize_keyboard= True
    )

@router.message(CommandStart())

async def start(message : Message):
    user_id = message.from_user.id
    ID_Channle = "-1003760258868"
    await message.answer(text="hi")
    if await check(user_id,ID_Channle) == True:
        await message.answer(text="به ربات خوش آمدید.",reply_markup= menu_Keybord())
    elif await check(user_id,ID_Channle) == False :
        await message.answer(text="لطفا برای استفاده از ربات در چنل ما عضو شوید.",reply_markup=checkmemeber_keyboard())

@router.callback_query(F.data == "checked")

async def check_again(call : CallbackQuery):
    ID_Channle = "-1003760258868"
    user_id = call.from_user.id
    if await check(user_id,ID_Channle) == True:
        await call.message.answer(text="به ربات خوش آمدید.",reply_markup= menu_Keybord())
        await call.answer(text="عشویت شما با موفقیت تایید شد.")
    elif await check(user_id,ID_Channle) == False :
        await call.message.answer(text="لطفا برای استفاده از ربات در چنل ما عضو شوید.",reply_markup=checkmemeber_keyboard())
        await call.answer(text="شما هنور در چنل عضو نشده اید")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

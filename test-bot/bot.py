import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("ربات اجرا شد ✅")

@dp.message(Command("file"))
async def send_file(msg: Message):
    file = FSInputFile("test.txt")
    await msg.answer_document(file)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

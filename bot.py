BOT_TOKEN = "123456789:ABCdefGhIJKlmNoPQRstUVwxyZ"

import asyncio, aiogram
from py_compile import main
from aiogram import Bot, Dispatcher, types
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
from aiogram.filters import Command
@dp.message(Command("start"))
async def command_start(message):
    await message.answer("Привіт! Я ваш бот для замовлень. Що ви хочете замовити?")
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
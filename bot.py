import asyncio, os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
load_dotenv("Keys.env")
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
from aiogram.filters import Command
@dp.message(Command("start"))
async def command_start(message):
    await message.answer("Привіт! Я ваш бот для замовлень. Що ви хочете замовити?")
async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

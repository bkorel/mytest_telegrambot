# main.py
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

# Получаем токен из переменной окружения (для безопасности)
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! 👋 Это мой первый бот на Render!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
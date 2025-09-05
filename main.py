from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Функция для создания клавиатуры
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help_button = types.KeyboardButton("Помощь 🆘")
    keyboard.add(help_button)
    return keyboard

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! 👋 Это мой первый бот на Render!",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "Я — твой первый бот! 🤖\nНажимай кнопки, чтобы общаться со мной.\nАвтор: ты сам 😉"
    )

# Обработчик нажатия на кнопку "Помощь 🆘"
@dp.message_handler(lambda message: message.text == "Помощь 🆘")
async def handle_help_button(message: types.Message):
    # Просто вызовем обработчик /help — переиспользуем логику!
    await send_help(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
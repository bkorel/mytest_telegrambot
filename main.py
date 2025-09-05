from aiogram import Bot, Dispatcher, types
import os
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Функция для создания клавиатуры
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help_button = types.KeyboardButton("Помощь 🆘")
    keyboard.add(help_button)
    return keyboard

# Обработчик команды /start
@dp.message(types.Message, commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! 👋 Это мой первый бот на Render!",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
@dp.message(types.Message, commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "Я — твой первый бот! 🤖\nНажимай кнопки, чтобы общаться со мной.\nАвтор: ты сам 😉"
    )

# Обработчик нажатия на кнопку "Помощь 🆘"
@dp.message(lambda message: message.text == "Помощь 🆘")
async def handle_help_button(message: types.Message):
    # Просто вызовем обработчик /help — переиспользуем логику!
    await send_help(message)

async def main():
    """Основная функция для запуска бота"""
    try:
        # Удаляем webhook если он был установлен
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
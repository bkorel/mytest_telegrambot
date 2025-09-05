from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для создания клавиатуры
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    help_button = types.KeyboardButton("Помощь 🆘")
    keyboard.add(help_button)
    return keyboard

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! 👋 Это мой первый бот на Render!",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
@dp.message(Command('help'))
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
        
        # Ждем немного, чтобы другие экземпляры завершились
        await asyncio.sleep(2)
        
        # Запускаем polling
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")
        # Если ошибка связана с конфликтом, ждем и пробуем еще раз
        if "TerminatedByOtherGetUpdates" in str(e):
            logging.info("Обнаружен конфликт с другим экземпляром бота. Ждем 10 секунд...")
            await asyncio.sleep(10)
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                await dp.start_polling(bot)
            except Exception as retry_error:
                logging.error(f"Ошибка при повторной попытке: {retry_error}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен пользователем")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
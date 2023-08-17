from settings.conf import BOT_API
from aiogram import Bot, Dispatcher, types

async def send_telegram_message(chat_id, text):
    bot = Bot(token=BOT_API)
    dispatcher = Dispatcher(bot)
    
    await bot.send_message(chat_id=chat_id, text=text)
    s = await bot.get_session()
    await s.close()
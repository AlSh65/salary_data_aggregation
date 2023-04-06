from aiogram import executor
from bot.handlers.aggregate_data import response_data
from bot.handlers.start import process_start_command
from bot.loader import dp

if __name__ == '__main__':
    dp.register_message_handler(process_start_command, commands=['start'])
    dp.register_message_handler(response_data, content_types=['text'])
    executor.start_polling(dp, skip_updates=True)

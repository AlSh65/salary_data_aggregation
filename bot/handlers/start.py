from aiogram.utils import executor

from bot.loader import dp
from aiogram import types


async def process_start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

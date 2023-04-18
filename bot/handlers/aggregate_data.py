import json
from aiogram import types
from bot.services.query_handler import get_aggregated_data
from bot.messages import  message_answer_exception

async def response_data(message: types.Message):
    try:
        user_data = json.loads(message.text)
        response = await get_aggregated_data(user_data)
        await message.answer(json.dumps(response))
    except Exception:
        await message.answer(message_answer_exception)


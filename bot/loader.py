import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
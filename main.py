from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
import asyncio
import logger

from bs4 import BeautifulSoup
import requests

from config import TOKEN
from utils import parse_cities

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler()
async def echo(message: types.Message):
    first_word = message.text.split()[0]

    if first_word == 'Салам':
        await message.answer("Алейкум")
    elif first_word == 'Привет':
        await message.answer("Хеллоу")
    
logger.info('Starting..')

executor.start_polling(dp, skip_updates=True)
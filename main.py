from email.headerregistry import BaseHeader
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext

from bs4 import BeautifulSoup
import requests

from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class WeatherForm(StatesGroup):
    city = State()

@dp.message_handler(commands=['weather'])
async def ask_city(message : types.Message):
    await WeatherForm.city.set()
    answer = await message.answer("В какой области вы находитесь?")

@dp.message_handler(state=WeatherForm.city)
async def get_cities(message : types.Message, state : FSMContext):
    source = 'https://world-weather.ru/pogoda/russia/'
    
    selected = message.text
    page = requests.get(source)
    soup = BeautifulSoup(page.text, 'lxml')
    
    ignore = ['Архив погоды', "Весь мир", 'Информеры', 'Пользовательское соглашение', 'Обратная связь', 'О проекте']
    cities = dict()

    list_items = soup.find_all('li')

    for item in list_items:
        city = item.find('a')

        if city is not None and city.text not in ignore:
            cities[city.text] = city.get('href')

    result = 'Не найдено'
    found = False

    for city in cities.keys():
        if selected in city:
            result = city
            found = True
            break

    if found:
        print(cities[result])
        
    

    await message.reply(f"Выбрана область : {result}")
    await state.finish()

@dp.message_handler()
async def echo(message: types.Message):
    first_word = message.text.split()[0]

    if first_word == 'Салам':
        await message.answer("Алейкум")
    elif first_word == 'Привет':
        await message.answer("Хеллоу")

print('Starting..')

executor.start_polling(dp, skip_updates=True)
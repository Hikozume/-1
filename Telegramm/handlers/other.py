from handlers import client
from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot_files import dp, bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_bd import cursor, cnxn

# Меню

btnStartSearch = KeyboardButton('Начать поиск')
btnMark = KeyboardButton('Марка автомобиля')
btnModel = KeyboardButton('Модель автомобиля')
specOffer = KeyboardButton('Эксклюзивное предложение')
filterOffers = KeyboardButton('Фильтр')
sorterOffers = KeyboardButton('Сортировка')
searchOffers = KeyboardButton('Поиск')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnStartSearch).row(btnMark, btnModel).add(specOffer).row(
    filterOffers, sorterOffers)


# Бд


async def message_to_coomand_start(message: types.Message):
    cursor.execute('SELECT * FROM UsersWithFilters')
    for line in cursor:
        res = line[1].split('_')
        client.dict_filter_tems[line[0]] = [res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]]
        client.dict_sorting_tems[line[0]] = line[2]
        client.dict_model_mark[line[0]] = ['Не задано', 'Не задано']

    if message.from_user.id not in client.dict_filter_tems:
        insert_query = '''INSERT INTO UsersWithFilters (id, filters, sorted) VALUES (?, ?, ?);'''
        cursor.execute(insert_query, message.from_user.id,
                       'Не задано_Не задано_Не задано_Не задано_Не задано_Не задано_Не задано_Не задано', 'actual')
        client.dict_filter_tems[message.from_user.id] = ['Не задано', 'Не задано', 'Не задано', 'Не задано',
                                                         'Не задано', 'Не задано', 'Не задано', 'Не задано']
        client.dict_sorting_tems[message.from_user.id] = 'actual'
        client.dict_model_mark[message.from_user.id] = ['Не задано', 'Не задано']
        cnxn.commit()

    await bot.send_message(message.from_user.id, 'Приветствую {0.first_name}'.format(message.from_user),
                           reply_markup=mainMenu)


def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(message_to_coomand_start, commands=['start'])

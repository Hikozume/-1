from aiogram.utils import executor
from aiogram import types
from bot_files import dp, bot
from handlers import client, other
from bot_bd import cursor, cnxn, cursor_auto
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image
from urllib.request import urlopen

other.reg_handlers_client(dp)
client.reg_handlers_client(dp)

empty_filter = 'Не задано_Не задано_Не задано_Не задано_Не задано_Не задано_Не задано_Не задано'
update_query = '''UPDATE UsersWithFilters SET filters = ? WHERE id = ?;'''
ads_to_show = 10
iter = 0
ads_from_bd = []


async def on_startup(_):
    cursor.execute('SELECT * FROM UsersWithFilters')
    for line in cursor:
        res = line[1].split('_')
        client.dict_filter_tems[line[0]] = [res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7]]
        client.dict_sorting_tems[line[0]] = line[2]
        client.dict_model_mark[line[0]] = ['Не задано', 'Не задано']
    print('Бот в сети')


@dp.callback_query_handler(text_startswith="sorter")
async def sorter_handler(callback: types.CallbackQuery):
    spl = callback.data.split('_')
    client.dict_sorting_tems[callback.from_user.id] = spl[1]
    cursor.execute("UPDATE UsersWithFilters SET sorted = ? WHERE id = ?", spl[1], callback.from_user.id)
    cnxn.commit()
    await callback.message.answer('Изменнены условия сортировки ' + spl[1])
    await callback.answer()


@dp.callback_query_handler(text_startswith="filter")
async def filter_handler(callback: types.CallbackQuery):
    spl = callback.data.split('_')
    if spl[1] == 'prise':
        await callback.message.answer('Введите диапазон стоимости по форме \nФорма: Цена От До \nПример: Цена 0 100000')
    if spl[1] == 'year':
        await callback.message.answer(
            'Введите диапазон года выпуска по форме \nФорма: Год От До \nПример: Год 2010 2014')
    if spl[1] == 'miles':
        await callback.message.answer(
            'Введите диапазон пробега автомобиля по форме \nПримичание: Пробег указывается в тыс.км \nФорма: Пробег От До \nПример: Пробег 2 10')
    if spl[1] == 'gearbox':
        linq_1 = types.InlineKeyboardButton('Автомат', callback_data='choose_gearbox1')
        linq_2 = types.InlineKeyboardButton('Механика', callback_data='choose_gearbox2')
        linq_3 = types.InlineKeyboardButton('Робот', callback_data='choose_gearbox3')
        linq_4 = types.InlineKeyboardButton('Вариатор', callback_data='choose_gearbox4')
        inline_gearbox = types.InlineKeyboardMarkup().add(linq_1).add(linq_2).add(linq_3).add(linq_4)
        await callback.message.answer('Выберите нужный тип коробки передач:', reply_markup=inline_gearbox)
    if spl[1] == 'engineV':
        linq_1 = types.InlineKeyboardButton('от 0.2л до 1.0л', callback_data='choose_engineV1')
        linq_2 = types.InlineKeyboardButton('от 1.0л до 1.8л', callback_data='choose_engineV2')
        linq_3 = types.InlineKeyboardButton('от 1.8л до 3.0л', callback_data='choose_engineV3')
        linq_4 = types.InlineKeyboardButton('от 3.0л до 10.0л', callback_data='choose_engineV4')
        inline_engineV = types.InlineKeyboardMarkup().add(linq_1).add(linq_2).add(linq_3).add(linq_4)
        await callback.message.answer('Выберите нужный объем двигателя:', reply_markup=inline_engineV)
    if spl[1] == 'power':
        await callback.message.answer(
            'Введите диапазон мощности автомобиля по форме \n Форма:Мощность От До \nПример: Мощность 110 130')
    if spl[1] == 'engineType':
        linq_1 = types.InlineKeyboardButton('Дизель', callback_data='choose_engineType1')
        linq_2 = types.InlineKeyboardButton('Бензин', callback_data='choose_engineType2')
        linq_3 = types.InlineKeyboardButton('Гибрид', callback_data='choose_engineType3')
        linq_4 = types.InlineKeyboardButton('Электро', callback_data='choose_engineType4')
        inline_engineType = types.InlineKeyboardMarkup().add(linq_1).add(linq_2).add(linq_3).add(linq_4)
        await callback.message.answer('Выберите нужный тип двигателя:', reply_markup=inline_engineType)
    if spl[1] == 'wheels':
        linq_1 = types.InlineKeyboardButton('Полный', callback_data='choose_wheels1')
        linq_2 = types.InlineKeyboardButton('Передний', callback_data='choose_wheels2')
        linq_3 = types.InlineKeyboardButton('Задний', callback_data='choose_wheels3')
        inline_wheels = types.InlineKeyboardMarkup().add(linq_1).add(linq_2).add(linq_3)
        await callback.message.answer('Выберите нужный привод автомобиля:', reply_markup=inline_wheels)
    await callback.answer()


@dp.callback_query_handler(text_startswith="choose_gearbox")
async def gearbox_handler(callback: types.CallbackQuery):
    filters_for_user = client.dict_filter_tems[callback.from_user.id]
    if callback.data.split('_')[1].endswith('1'):
        filters_for_user[3] = 'АКПП'
    if callback.data.split('_')[1].endswith('2'):
        filters_for_user[3] = 'механика'
    if callback.data.split('_')[1].endswith('3'):
        filters_for_user[3] = 'робот'
    if callback.data.split('_')[1].endswith('4'):
        filters_for_user[3] = 'вариатор'
    cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",
                   filters_for_user[0] + '_' + filters_for_user[1] + '_' + filters_for_user[2] + '_' + filters_for_user[
                       3] + '_' + filters_for_user[4] + '_' + filters_for_user[5] + '_' + filters_for_user[6] + '_' +
                   filters_for_user[7],
                   callback.from_user.id)
    cnxn.commit()
    await callback.message.answer('Условия фильтрации изменены')
    await callback.answer()


@dp.callback_query_handler(text_startswith="choose_engineV")
async def engineV_handler(callback: types.CallbackQuery):
    filters_for_user = client.dict_filter_tems[callback.from_user.id]
    if callback.data.split('_')[1].endswith('1'):
        filters_for_user[4] = 'от 0.2 до 1.0'
    if callback.data.split('_')[1].endswith('2'):
        filters_for_user[4] = 'от 1.0 до 1.8'
    if callback.data.split('_')[1].endswith('3'):
        filters_for_user[4] = 'от 1.8 до 3.0'
    if callback.data.split('_')[1].endswith('4'):
        filters_for_user[4] = 'от 3.0 до 10.0'
    cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",
                   filters_for_user[0] + '_' + filters_for_user[1] + '_' + filters_for_user[2] + '_' + filters_for_user[
                       3] + '_' + filters_for_user[4] + '_' + filters_for_user[5] + '_' + filters_for_user[6] + '_' +
                   filters_for_user[7],
                   callback.from_user.id)
    cnxn.commit()
    await callback.message.answer('Условия фильтрации изменены')
    await callback.answer()


@dp.callback_query_handler(text_startswith="choose_engineType")
async def engineV_handler(callback: types.CallbackQuery):
    filters_for_user = client.dict_filter_tems[callback.from_user.id]
    if callback.data.split('_')[1].endswith('1'):
        filters_for_user[6] = 'дизель'
    if callback.data.split('_')[1].endswith('2'):
        filters_for_user[6] = 'бензин'
    if callback.data.split('_')[1].endswith('3'):
        filters_for_user[6] = 'гибрид'
    if callback.data.split('_')[1].endswith('4'):
        filters_for_user[6] = 'электро'
    cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",
                   filters_for_user[0] + '_' + filters_for_user[1] + '_' + filters_for_user[2] + '_' + filters_for_user[
                       3] + '_' + filters_for_user[4] + '_' + filters_for_user[5] + '_' + filters_for_user[6] + '_' +
                   filters_for_user[7],
                   callback.from_user.id)
    cnxn.commit()
    await callback.message.answer('Условия фильтрации изменены')
    await callback.answer()


@dp.callback_query_handler(text_startswith="choose_wheels")
async def engineV_handler(callback: types.CallbackQuery):
    filters_for_user = client.dict_filter_tems[callback.from_user.id]
    if callback.data.split('_')[1].endswith('1'):
        filters_for_user[7] = '4WD'
    if callback.data.split('_')[1].endswith('2'):
        filters_for_user[7] = 'передний'
    if callback.data.split('_')[1].endswith('3'):
        filters_for_user[7] = 'задний'
    cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",
                   filters_for_user[0] + '_' + filters_for_user[1] + '_' + filters_for_user[2] + '_' + filters_for_user[
                       3] + '_' + filters_for_user[4] + '_' + filters_for_user[5] + '_' + filters_for_user[6] + '_' +
                   filters_for_user[7],
                   callback.from_user.id)
    cnxn.commit()
    await callback.message.answer('Условия фильтрации изменены')
    await callback.answer()


@dp.callback_query_handler(text_startswith="all_reset")
async def gearbox_handler(callback: types.CallbackQuery):
    client.dict_filter_tems[callback.from_user.id] = ['Не задано', 'Не задано', 'Не задано', 'Не задано', 'Не задано',
                                                      'Не задано', 'Не задано', 'Не задано']
    client.dict_sorting_tems[callback.from_user.id] = 'actual'
    client.dict_model_mark[callback.from_user.id] = ['Не задано', 'Не задано']
    cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?", empty_filter, callback.from_user.id)
    cnxn.commit()
    cursor.execute("UPDATE UsersWithFilters SET sorted = ? WHERE id = ?", 'actual', callback.from_user.id)
    cnxn.commit()
    await callback.message.answer('Условия фильтрации изменены')
    await callback.answer()


@dp.callback_query_handler(text_startswith="model_")
async def gearbox_handler(callback: types.CallbackQuery):
    client.dict_model_mark[callback.from_user.id][1] = callback.data.split('_')[1]
    await callback.message.answer('Выбрана модель: ' + callback.data.split('_')[1])
    await callback.answer()


@dp.callback_query_handler(text_startswith="find_cars")
async def gearbox_handler(callback: types.CallbackQuery):
    get_cars_query = '''SELECT * FROM AUTOS WHERE'''
    data_for_analytics = '''INSERT INTO Analytics (Mark, Model, filter, sorted) VALUES (?, ?, ?, ?)'''
    query_filters = '''SELECT * FROM UsersWithFilters WHERE id = ?'''

    cursor.execute(query_filters, callback.from_user.id)
    analytics_filter = ''
    for row in cursor:
        analytics_filter = row[1]
    cursor.execute(data_for_analytics, client.dict_model_mark[callback.from_user.id][0],
                   client.dict_model_mark[callback.from_user.id][1],
                   analytics_filter,
                   client.dict_sorting_tems[callback.from_user.id])
    cursor.commit()

    i = 0
    for filter in client.dict_filter_tems[callback.from_user.id]:
        if filter != 'Не задано':
            if i == 0:
                get_cars_query += ' Price >= ' + filter.split(':')[0] + ' AND Price <= ' + filter.split(':')[1]
                get_cars_query += ' AND '
            if i == 1:
                get_cars_query += ' Year >= ' + filter.split(':')[0] + ' AND Year <= ' + filter.split(':')[1]
                get_cars_query += ' AND '
            if i == 2:
                get_cars_query += ' Milage >= ' + filter.split(':')[0] + ' AND Milage <= ' + filter.split(':')[1]
                get_cars_query += ' AND '
            if i == 3:
                get_cars_query += ' Transmission = ' + "'" + filter + "' "
                get_cars_query += ' AND '
            if i == 4:
                get_cars_query += " EngineCapacity >= '" + filter.split(' ')[1] + "' AND EngineCapacity <= '" + \
                                   filter.split(' ')[3] + "' "
                get_cars_query += ' AND '
            if i == 5:
                get_cars_query += ' EnginePower >= ' + filter.split(':')[0] + ' AND EnginePower <= ' + \
                                  filter.split(':')[1]
                get_cars_query += ' AND '
            if i == 6:
                get_cars_query += ' FuelType = ' + "'" + filter + "' "
                get_cars_query += ' AND '
            if i == 7:
                get_cars_query += ' DriveWheels = ' + "'" + filter + "' "
                get_cars_query += ' AND '
        i += 1

    if client.dict_model_mark[callback.from_user.id] != ['Не задано', 'Не задано']:
        get_cars_query += " Mark = '" + client.dict_model_mark[callback.from_user.id][0] + "'"
        get_cars_query += ' AND '
    if client.dict_model_mark[callback.from_user.id][1] != 'Не задано':
        get_cars_query += " Model = '" + client.dict_model_mark[callback.from_user.id][1] + "'"
        get_cars_query += ' AND '
    if get_cars_query.endswith(' AND '):
        get_cars_query = get_cars_query[:-4]
    if get_cars_query.endswith(' WHERE'):
        get_cars_query = get_cars_query[:-6]
    if client.dict_sorting_tems[callback.from_user.id] != 'actual':
        if client.dict_sorting_tems[callback.from_user.id].endswith('1'):
            get_cars_query += ' ORDER BY ' + client.dict_sorting_tems[callback.from_user.id][0:-1]
        else:
            get_cars_query += ' ORDER BY ' + client.dict_sorting_tems[callback.from_user.id][0:-1] + ' DESC'

    print(get_cars_query)
    cursor_auto.execute(get_cars_query)

    global ads_to_show
    ads_to_show = 10
    global iter
    iter = 0

    for i, row in enumerate(cursor_auto):
            ads_from_bd.append(row)
    await ads(callback.from_user.id)
    await callback.answer()

async def ads(id: int):
    global iter
    for i, row in enumerate(ads_from_bd):
        if i < ads_to_show and i >= iter:
            linq_auto = InlineKeyboardMarkup().add(InlineKeyboardButton('Ссылка', url=row[4]))
            await bot.send_photo(id, photo=row[12], caption='Марка: ' + row[1] + '\n'
                                                               + ' Модель: ' + row[2] + '\n'
                                                               + 'Год выпуска: ' + str(row[3]) + '\n'
                                                               + 'Объем двигателя: ' + str(row[5]) + '\n'
                                                               + 'Мощность: ' + str(row[6]) + ' л.с\n'
                                                               + 'Тип двигателя: ' + row[7] + '\n'
                                                               + 'Коробка передач: ' + row[8] + '\n'
                                                               + 'Привод: ' + row[9] + '\n'
                                                               + 'Пробег: ' + str(row[10]) + '\n'
                                                               + 'Цена: ' + str(row[11]) + '\n'
                                                               + 'Местоположение: ' + str(row[13]) + '\n',
                                                                reply_markup=linq_auto)
        if i == ads_to_show:
            iter = i
            show_more = InlineKeyboardMarkup().add(InlineKeyboardButton('Да', callback_data='show_ads'))
            await bot.send_message(id, text='Показать больше?', reply_markup=show_more)

@dp.callback_query_handler(text='show_ads')
async def gearbox_handler(callback: types.CallbackQuery):
    global ads_to_show
    ads_to_show += 10
    await ads(callback.from_user.id)
    await callback.answer()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

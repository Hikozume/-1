from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot_files import dp, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_bd import cursor, cnxn

dict_filter_tems = {1: [None, None, None, None, None, None, None, None]}
dict_sorting_tems = {1: 'actual'}
dict_model_mark = {1: [None, None]}


#Инлайн

linq = InlineKeyboardButton('Ссылка', url='https://auto.ru/cars/used/sale/land_rover/defender/1115015973-34a87fd7/')
inline_kb1 = InlineKeyboardMarkup().add(linq)

async def message_to_coomand_help(message : types.Message):
    await bot.send_message(message.from_user.id, 'Какая-то информация')

async def message_sticker_handler(message: types.Message):
    file_unique_id = message.sticker.file_unique_id
    file_sticker_id = open('Auto.txt', 'r')
    for line in file_sticker_id:
        splited = line.split(":")
        if(splited[1][0:-2] == file_unique_id[0:-1]):
            dict_model_mark[message.from_user.id] = [splited[0], 'Не задано']
            await bot.send_message(message.from_user.id, 'Вы выбрали марку ' + splited[0])

async def echo_send(message : types.Message):
    if message.text == 'Марка автомобиля':
        await bot.send_message(message.from_user.id, 'Отправте стикер с маркой авто')
        await bot.send_message(message.from_user.id, 'Стикеры можно получить по ссылке:' + '\n tg://addstickers?set=Autologo')

    if message.text == 'Модель автомобиля':
        if dict_model_mark[message.from_user.id][0] == 'Не задано':
            await bot.send_message(message.from_user.id, 'Сначала выберите марку автомобиля')
        else:
            cursor.execute("SELECT Model FROM MarkAndModels WHERE Mark = ?", dict_model_mark[message.from_user.id][0])
            inline_model = InlineKeyboardMarkup(row_width=3)
            for model in cursor:
                inline_model.insert(InlineKeyboardButton(model[0], callback_data='model_'+ model[0]))
            await bot.send_message(message.from_user.id, 'Сделайте выбор модели для выбранной марки ('+ dict_model_mark[message.from_user.id][0] + ')', reply_markup=inline_model)


    if message.text == 'Эксклюзивное предложение':
        photo = open(r"C:\Users\Admin\Pictures\Defender.jpg", 'rb')
        await bot.send_photo(message.from_user.id, photo=photo)
        await bot.send_message(message.from_user.id, 'Land Rover Defender 2021 \n3.0 л / 249 л.с. / Дизель \nКомплектация HSE \nПробег 15000 км. \nЦена: 16.230.000', reply_markup=inline_kb1)

    if message.text == 'Сортировка':
        linq_1 = InlineKeyboardButton('По возрастанию цены', callback_data='sorter_Pri`ce1')
        linq_2 = InlineKeyboardButton('По убыванию цены', callback_data='sorter_Price2')
        linq_3 = InlineKeyboardButton('По году, старше', callback_data='sorter_Year1')
        linq_4 = InlineKeyboardButton('По году, новее', callback_data='sorter_Year2')
        linq_5 = InlineKeyboardButton('По актуальности', callback_data='sorter_actual')
        inline_sorting = InlineKeyboardMarkup().add(linq_1).add(linq_2).add(linq_3).add(linq_4).add(linq_5)
        await bot.send_message(message.from_user.id, 'Выберите условия фильтрации: ', reply_markup=inline_sorting)

    if message.text == 'Фильтр':
        linq_1 = InlineKeyboardButton('Цена', callback_data='filter_prise')
        linq_2 = InlineKeyboardButton('Год выпуска', callback_data='filter_year')
        linq_3 = InlineKeyboardButton('Пробег', callback_data='filter_miles')
        linq_4 = InlineKeyboardButton('Коробка', callback_data='filter_gearbox')
        linq_5 = InlineKeyboardButton('Объем двигателя', callback_data='filter_engineV')
        linq_6 = InlineKeyboardButton('Мощность', callback_data='filter_power')
        linq_7 = InlineKeyboardButton('Тип двигателя', callback_data='filter_engineType')
        linq_8 = InlineKeyboardButton('Привод', callback_data='filter_wheels')
        inline_filter = InlineKeyboardMarkup().add(linq_1).add(linq_2).add(linq_3).add(linq_4).add(linq_5).add(linq_6).add(linq_7).add(linq_8)
        await bot.send_message(message.from_user.id, 'Выберите условия фильтрации:', reply_markup=inline_filter)

    if message.text == 'Начать поиск':
        filter_for_user = dict_filter_tems[message.from_user.id]
        linq_reset = InlineKeyboardMarkup().add(InlineKeyboardButton('Начать поиск объявлений', callback_data='find_cars')).\
            add(InlineKeyboardButton('Сбросить условия поиска объявлений', callback_data='all_reset'))
        await bot.send_message(message.from_user.id, '*Текущие условия поиска объявлений* \nЦена автомобиля: \t' + filter_for_user[0]
        + '\nВыбранная марка: \t' + dict_model_mark[message.from_user.id][0]
        + '\nВыбранная модель: \t' + dict_model_mark[message.from_user.id][1]
        + '\nВыбранный год выпуска: \t' + filter_for_user[1]
        + '\nПробег автомобиля: \t' + filter_for_user[2]
        + '\nТип коробка передач: \t' + filter_for_user[3]
        + '\nОбъем двигателя: \t' + filter_for_user[4]
        + '\nМощность двигателя: \t' + filter_for_user[5]
        + '\nТип двигателя: \t' + filter_for_user[6]
        + '\nТип привода: \t' + filter_for_user[7]
        + '\nСортировка: \t' + dict_sorting_tems[message.from_user.id], parse_mode=types.ParseMode.MARKDOWN, reply_markup=linq_reset)

        
    if message.text.startswith('Цена') or message.text.startswith('цена'):
        query_string = message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        filter_for_user = dict_filter_tems[message.from_user.id]
        dict_filter_tems[message.from_user.id][0] =  message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?", 
            query_string + '_' + filter_for_user[1] + '_' + filter_for_user[2] + '_' + filter_for_user[3] + '_' + filter_for_user[4] + '_' + filter_for_user[5] + '_' + filter_for_user[6] + '_' + filter_for_user[7], 
            message.from_user.id)
        cnxn.commit()
        await bot.send_message(message.from_user.id, 'Условия фильтрации изменены')

    if message.text.startswith('Год') or message.text.startswith('год'):
        query_string = message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        filter_for_user = dict_filter_tems[message.from_user.id]
        dict_filter_tems[message.from_user.id][1] = message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",
            filter_for_user[0] + '_' + query_string + '_' + filter_for_user[2] + '_' + filter_for_user[3] + '_' + filter_for_user[4] + '_' + filter_for_user[5] + '_' + filter_for_user[6] + '_' + filter_for_user[7], 
            message.from_user.id)
        cnxn.commit()
        await bot.send_message(message.from_user.id, 'Условия фильтрации изменены')
        
    if message.text.startswith('Пробег') or message.text.startswith('пробег'):
        query_string = message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        filter_for_user = dict_filter_tems[message.from_user.id]
        dict_filter_tems[message.from_user.id][2] =  message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",
            filter_for_user[0] + '_' + filter_for_user[1] + '_' + query_string + '_' + filter_for_user[3] + '_' + filter_for_user[4] + '_' + filter_for_user[5] + '_' + filter_for_user[6] + '_' + filter_for_user[7], 
            message.from_user.id)
        cnxn.commit()
        await bot.send_message(message.from_user.id, 'Условия фильтрации изменены')

    if message.text.startswith('Мощность') or message.text.startswith('мощность'):
        query_string = message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        filter_for_user = dict_filter_tems[message.from_user.id]
        dict_filter_tems[message.from_user.id][5] = message.text.split(' ')[1] + ':' + message.text.split(' ')[2]
        cursor.execute("UPDATE UsersWithFilters SET filters = ? WHERE id = ?",            
            filter_for_user[0] + '_' + filter_for_user[1] + '_' + filter_for_user[2] + '_' + filter_for_user[3] + '_' + filter_for_user[4] + '_' + query_string + '_' + filter_for_user[6] + '_' + filter_for_user[7], 
            message.from_user.id)
        cnxn.commit()
        await bot.send_message(message.from_user.id, 'Условия фильтрации изменены')

def reg_handlers_client(dp: Dispatcher):
    dp.register_message_handler(message_to_coomand_help, commands = ['help'])
    dp.register_message_handler(message_sticker_handler, content_types=['sticker'])
    dp.register_message_handler(echo_send)
    
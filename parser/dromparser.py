import aiohttp
from bs4 import BeautifulSoup
from car import Car
import fake_useragent
from datebase import DateBase


links = []
wheelDrives = ["4WD", "передний", "задний"]
transmissions = ["автомат", "АКПП", "робот", "вариатор", "механика"]
fuelTypes = ["бензин", "дизель", "электро", "гибрид", "ГБО"]
lst = ['Aston Martin', 'Land Rover', 'Alfa Romeo', 'DW Hower', 'Great Wall', 'Iran Khodro']
datebase = DateBase(r'Autos.db') #создаем объект класса database


async def parse(price1, price2, limitprice, step=2000): #функция для парсинга со входными данными, начальная цена, конечная цена, лимит и шаг
    page = 1
    while True:
        url = f'https://auto.drom.ru/all/page{page}/?minprice={price1}&maxprice={price2}&damaged=2&unsold=1&ph=1'
        user = fake_useragent.UserAgent().random #рандомные юзер агенты для запросов
        headers = {'user-agent': user}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                request = await resp.text()
        soup = BeautifulSoup(request, 'lxml') #далее обращаясь к объекту BS находим нужные нам элементу по тегу и классу
        if soup.find(class_='css-1173kvb eaczv700') is None:
            if price2 >= limitprice:
                return
            page = 1
            price1 = price2 + 1
            price2 += step
            print(f'{price1} - {price2}')
            continue
        else:
            offers = soup.find_all('a', class_='css-1ctbluq ewrty961')
            for el in offers:
                car = Car()
                name = el.find('div', class_='css-17lk78h e3f4v4l2').text.split(',')
                mark_and_model = name[0].split()
                car.mark = mark_and_model[0]
                car.model = ' '.join(mark_and_model[1:len(mark_and_model)])
                temp_lst = [i for i in lst if i.count(car.mark) > 0]
                if temp_lst:
                    car.mark = temp_lst[0]
                    car.model = ' '.join(mark_and_model[2:len(mark_and_model)])
                car.year = int(name[1])
                tech_specs = el.find('div', class_='css-188tlrp e162wx9x0').find_all('span')
                car.link = el['href']
                if car.link in links:
                    with open('samelinks.txt', 'a') as file:
                        file.write(car.link + '\n')
                        car = None
                        continue
                links.append(car.link)
                try:
                    engine = tech_specs[0].text.replace(',', '').split()
                    for z in range(len(engine)):
                        if engine[z] == 'л':
                            car.engineCapacity = float(engine[z-1])
                        if engine[z] == 'л.с.)' or engine[z] == 'л.с.':
                            car.power = int(engine[z-1].replace('(', ''))
                    for i in range(len(tech_specs)):
                        string = tech_specs[i].text.replace(',', '')
                        if string in fuelTypes:
                            car.fuelType = string
                        elif string in transmissions:
                            car.transmission = string
                        elif string in wheelDrives:
                            car.driveWheels = string
                        elif "км" in string:
                            milage = 0
                            milage_list = string.split()
                            if milage_list[1] == 'тыс.':
                                milage = int(milage_list[0] + '000')
                            car.milage = milage
                except:
                    pass
                price_of_car = el.find('span', class_='css-byj1dh e162wx9x0').text.split()
                price_of_car = int(''.join(price_of_car[:len(price_of_car)-1]))
                car.price = price_of_car
                try:
                    images_str = el.find(class_='css-11n001v e1e9ee560').find('img')['data-srcset']
                    images = images_str.split(',')
                    car.image = images[1].split()[0]
                except:
                    car.image = el.find(class_='css-11n001v e1e9ee560').find('img')['data-src']
                car.location = el.find(class_='css-1mj3yjd e162wx9x0').text
                values = car.mark, car.model, car.year, car.link, car.engineCapacity, car.power, car.fuelType, car.transmission, car.driveWheels, car.milage, car.price,car.image, car.location
                datebase.add_record('Auto', values) #записываем в базу объявление
                print(car.link)
                car = None
        page += 1

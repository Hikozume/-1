import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from car import Car
from datebase import DateBase
import cfscrape



datebase = DateBase('DESKTOP-SI0JD8G', 'Auto')
scraper = cfscrape.create_scraper()
transmissionTypes = ['AT', 'MT']
driveWheel_types = [' передний', ' задний', ' полный']
fuelTypes = [' бензин', ' дизель']
links = []
lst = ['Aston Martin', 'Land Rover', 'Alfa Romeo', 'DW Hower', 'Great Wall', 'Iran Khodro']


async def parse_avito(price1, price2, limitprice, step=2000):
    page = 1
    while True:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(r"C:\Users\HENNESSY-\Desktop\chromedriver.exe", options=options)
        default_url = 'https://www.avito.ru/rossiya/avtomobili?cd=1&f=ASgBAQICAUTyCrCKAQFA9sQNFL6wOg'
        driver.get(default_url)
        time.sleep(2)
        prices = driver.find_element(By.CLASS_NAME, 'group-root-DENYm').find_elements(By.CLASS_NAME, 'input-input-Zpzc1')
        prices[0].send_keys(price1)
        prices[1].send_keys(price2)
        accept_button = driver.find_element(By.CLASS_NAME, 'styles-box-rgPSN')
        accept_button.click()
        url = driver.current_url
        driver.close()
        for i in range(1, 101):  #проверить переход по страницам, ощущение будто фильтры меняются быстрее чем скрипт ободйет все результаты
            request = scraper.get(url+f"&p={i}")
            print(f'[INFO] {url+f"&p={i}"}')
            print(request.status_code)
            soup = BeautifulSoup(request.text, 'lxml')
            items_list = soup.find(class_='items-items-kAJAg')
            if items_list.text == '':
                if price2 == limitprice:
                    return
                page = 1
                price1 = price2 + 1
                price2 += step
                print(f'{price1} - {price2}')
                break
            else:
                offers = soup.find_all(class_='iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum')
                for el in offers:
                    car = Car()
                    car.link = f'https://www.avito.ru{el.find("a")["href"]}'
                    if car.link in links:
                        with open('samelinks.txt', 'a') as file:
                            file.write(car.link + '\n')
                            continue
                    links.append(car.link)
                    name = el.find('h3').text.split(',')
                    mark_and_model = name[0].split()
                    car.mark = mark_and_model[0]
                    car.model = ' '.join(mark_and_model[1:len(mark_and_model)])
                    temp_lst = [i for i in lst if i.count(car.mark) > 0]
                    if temp_lst:
                        car.mark = temp_lst[0]
                        car.model = ' '.join(mark_and_model[2:len(mark_and_model)])
                    car.year = int(name[1])
                    price_of_car = el.find(class_='price-text-_YGDY text-text-LurtD text-size-s-BxGpL').text.split()
                    car.price = int(''.join(price_of_car[:len(price_of_car) - 1]))
                    tech_params = el.find(class_='iva-item-text-Ge6dR text-text-LurtD text-size-s-BxGpL').text.split(',')
                    for param in tech_params:
                        if transmissionTypes[0] in param or transmissionTypes[1] in param:  #доделать проверку!! обЪема двигателя или каких-то еще параметров может не быть
                            engine_transmission = param.split()
                            for value in engine_transmission:
                                if value in transmissionTypes:
                                    transmission = value
                                elif len(engine_transmission) == 4:
                                    car.engineCapacity = float(engine_transmission[0])
                                    car.enginePower = int(engine_transmission[2].replace('(', '').replace(' л.с)', ''))
                                    transmission = engine_transmission[1]
                                    break
                            if transmission == 'MT':
                                car.transmission = "механика"
                            elif transmission == 'AT':
                                car.transmission = 'автомат'
                        elif "км" in param:
                            milage_list = param.split()
                            car.milage = ''.join(milage_list[:len(milage_list) - 1])
                        elif param in driveWheel_types:
                            car.driveWheels = param
                        elif param in fuelTypes:
                            car.fuelType = param
                        else:
                            pass
                    locationAddress = el.find(class_='geo-address-fhHd0 text-text-LurtD text-size-s-BxGpL').text.split(',')
                    car.location = locationAddress[len(locationAddress)-1]
                    car.image = el.find('li')['data-marker'].split('-')[2]
                    values = car.mark, car.model, car.year, car.link, car.engineCapacity, car.power, car.fuelType, car.transmission, car.driveWheels, car.milage, car.price, car.image, car.location
                    datebase.add_record('Auto', values)
                    print(car.link)
                    car = None
            page += 1

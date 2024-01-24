from bs4 import BeautifulSoup
import datetime
import requests
import re

from save_to_db import insert_data

url = 'https://auto.ria.com/uk/car/used/'

list_data = []


def get_data(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def get_cars_current_page():
    soup = get_data(url)
    items = soup.find_all('section', class_='ticket-item')
    get_next_page()
    get_car_info(items)


def get_next_page():
    global url
    soup = get_data(url)
    page_count = soup.find('a', class_='page-link js-next')
    url = page_count.get('href')
    return page_count.get('href')


def get_car_info(items):
    for item in items:
        url_car = item.find('a', class_='m-link-ticket')
        title_car = item.find('a', class_='address')
        price_car = item.find(attrs={'data-currency': "USD"}).text
        race_car = item.find('li', class_='js-race').text
        car_num = item.find('span', class_='state-num')
        vin_num = item.find('span', class_='label-vin')

        car_link = requests.get(url_car.get('href')).text
        current_car_html = BeautifulSoup(car_link, 'html.parser')
        saller_name = current_car_html.find('div', class_='seller_info_name')

        image_car = current_car_html.find('img', class_='m-auto').get('src')
        img_count = current_car_html.find('a', class_='show-all')

        race_int = re.search(r'\b(\d+)\b', race_car)
        odometer = int(race_int.group(1)) * 1000

        if saller_name:
            seller_name_text = saller_name.get_text()
        else:
            seller_name_text = None

        if car_num:
            car_number = car_num.contents[0].strip()
        else:
            car_number = None

        if vin_num:
            car_vin = vin_num.find('span').text
        else:
            car_vin = None

        if img_count:
            img_count_int = re.search(r'\b(\d+)\b', img_count.get_text())
            images_count = int(img_count_int.group(1))
        else:
            images_count = None

        map = {
            "url": url_car.get('href'),
            "title": title_car.find('span', class_='blue').text,
            'price_usd': int(price_car.replace(' ', '')),
            'odometer': odometer,
            'username': seller_name_text,
            'phone_number': '',  # Need to rework
            'image_url': image_car,
            'images_count': images_count,
            'car_number': car_number,
            'car_vin': car_vin
        }

        datetime_found = datetime.datetime.now()

        data = (
            url_car.get('href'),
            title_car.find('span', class_='blue').text,
            int(price_car.replace(' ', '')),
            odometer,
            seller_name_text,
            None,
            image_car,
            images_count,
            car_number,
            car_vin,
            datetime_found,
        )

        insert_data(data)
        list_data.append(map)
    print(list_data)

    get_cars_current_page()
    return list_data

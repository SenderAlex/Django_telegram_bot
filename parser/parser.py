
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg2

class Parser:
    db_name = 'av_by_data_bases'
    user = 'av_by_admin'
    password = 'AVLioneLMessI1024BY'
    host = 'localhost'
    port = '5432'
    base_url = 'https://cars.av.by'
    extra_url = '/filter?price_usd[max]='


    @staticmethod
    def get_player_by_link(base_url, extra_url):
        data = []
        flag = True
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0'}
        while flag:
            response = requests.get(base_url+extra_url, headers=headers)
            html = response.text

            html_rating = BeautifulSoup(html, 'html.parser')
            next_page = html_rating.find('a', class_="button button--default button--loading")

            if next_page != None:
                extra_url = next_page.attrs['href']
            else:
                flag = False

            cars = (html_rating.find('div', class_='listing__items'))

            for car in cars:
                title = car.find_next('span', class_="link-text").text.replace('\xa0', '').replace('\'', '')
                data.append(title)
                photo = car.find_next('div', class_="listing-item__wrap").img["data-src"]
                data.append(photo)
                description = ((car.find_next('div', class_="listing-item__params").text.
                               replace('\n', '').replace('\xa0', '').
                               replace('г.', 'г, ').replace('\u2009', '').
                               replace('г.', ' г,').replace('л', ' л').
                               replace('г.', ' г,').replace('л', ' л').
                               replace('  ', ' ').replace('≈', '').
                               replace('$', '').replace('р.', '').
                               replace(' л', 'л').replace('г', '').
                               replace('л', '').replace('км', '')))
                descrip = description.split(',')
                data.extend(descrip)
                price = ((car.find_next('div', class_="listing-item__price").text.replace('\xa0', '').
                         replace('р.', ' р.').replace('\u2009', '').
                         replace(' р.', '')))
                data.append(price)
                price_usd = ((car.find_next('div', class_="listing-item__priceusd").text.replace('\u2009', '').
                             replace('\xa0', '').replace('$', '$').
                             replace('≈', '').replace('$', '')))
                data.append(price_usd)
                location = car.find_next('div', class_="listing-item__location").text
                data.append(location)
                link = car.find_next('a', class_="listing-item__link")
                full_link = f'https://cars.av.by{link["href"]}'
                data.append(full_link)

        full_data = [tuple(data[i:i+11]) for i in range(0, len(data), 11)]
        # for item in full_data:
        #     print(item)
        #     print()
        return full_data

    def create_connection(self):  # подключение к БД
        connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db_name
        )
        return connection

    def create_car_table(self, connection):
        with connection.cursor() as cursor:
            # cursor.execute("""
            # TRUNCATE TABLE tele_bot_app_car
            # """
            # )
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS tele_bot_app_car
                    (
                        id serial PRIMARY KEY,
                        title text,
                        photo text,
                        year integer,
                        transmission text,
                        engine text,
                        engine_type text,
                        body_type_mileage text,
                        price_BYN integer,
                        price_USD integer,
                        city text,
                        http_link text
                    )

                """
            )
            connection.commit()
            print("Table created successfully")

########################################################################################
    def insert(self, connection, full_data):
        cursor = connection.cursor()
        for data in full_data:
            cursor.execute(f"INSERT INTO tele_bot_app_car (title, photo, year, transmission, engine, engine_type,"
                           f" body_type_mileage, price_BYN, price_USD, city, http_link) VALUES"
                           f" ('{(data[0])}', '{data[1]}', {int(data[2])},  '{data[3]}', '{data[4]}', '{data[5]}',"
                           f" '{data[6]}', {int(data[7])}, {int(data[8])}, '{data[9]}', '{data[10]}')")
        connection.commit()


    def save_to_postgres(self, full_data):
        connection = self.create_connection()
        self.create_car_table(connection)
        self.insert(connection, full_data)


    def run(self):
        begin_time = datetime.now()
        car_items = self.get_player_by_link(Parser.base_url, Parser.extra_url)
        print(car_items)
        connection = self.create_connection()
        self.create_car_table(connection)
        self.insert(connection, car_items)
        self.save_to_postgres(car_items)
        end_time = datetime.now()
        execute_time = end_time - begin_time
        print(f"Время получения данных {execute_time}")


Parser().run()



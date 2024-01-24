from get_car_info import get_car_info, get_cars_current_page
from save_to_db import create_table, dump_db
import schedule
import time


def start():
    print("Parsing started")
    create_table()
    get_cars_current_page()


def dump():
    dump_db('dumps/dump_file.backup')


if __name__ == "__main__":
    schedule.every().day.at("12:00").do(start)
    schedule.every().day.at("00:00").do(dump)

    while True:
        schedule.run_pending()
        time.sleep(1)

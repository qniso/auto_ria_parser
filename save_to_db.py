import subprocess

import psycopg2
from config import host, user, password, db_name

def get_connection():
    return psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password,
        port=5432
    )

def create_table():
    create_table_auto_ria = '''
        CREATE TABLE IF NOT EXISTS auto_ria (
            id SERIAL PRIMARY KEY,
            url VARCHAR(255),
            title VARCHAR(255),
            price_usd NUMERIC,
            odometer NUMERIC,
            username VARCHAR(255),
            phone_number VARCHAR(15),
            image_url VARCHAR(255),
            images_count NUMERIC,
            car_number VARCHAR(20),
            car_vin VARCHAR(50),
            datetime_found TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    '''
    with get_connection() as connection, connection.cursor() as cursor:
        try:
            cursor.execute(create_table_auto_ria)
            connection.commit()
        except Exception as error:
            print(f"Error: {error}")

def insert_data(data):
    insert_data_query = '''
        INSERT INTO auto_ria (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    with get_connection() as connection, connection.cursor() as cursor:
        try:
            cursor.execute(insert_data_query, data)
            connection.commit()
        except Exception as error:
            print(f"Error: {error}")


def dump_db(output_file):
    dump_command = f'"C:/Program Files/PostgreSQL/16/bin/pg_dump.exe" -h 127.0.0.1 -U postgres -d {db_name} -F c -b -v -f "{output_file}"'


    try:
        subprocess.run(dump_command, shell=True, check=True)
        print(f"Database dumped successfully to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error dumping database: {e}")


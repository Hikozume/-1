import sqlite3

#класс работы с бд, с методами очистить таблицу, добавить запись, создать таблицу
class DateBase:
    connection_to_db = None
    cursor = None

    def __init__(self, database_name):
        self.connection_to_db = sqlite3.connect(fr'{database_name}')
        self.cursor = self.connection_to_db.cursor()

    def clear_table(self, table_name):
        self.cursor.execute(f'DELETE FROM {table_name}')
        self.connection_to_db.commit()

    def add_record(self, table_name, values):
        query = f"INSERT INTO {table_name} (Mark, Model, Year, Link, EngineCapacity, EnginePower, FuelType, Transmission, DriveWheels,Milage, Price, Image, Location) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"
        self.cursor.execute(query, values)
        self.connection_to_db.commit()

    def create_table(self, query):
        self.cursor.execute(query)
        self.connection_to_db.commit()




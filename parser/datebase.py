import pyodbc


class DateBase:
    connection_to_db = None
    cursor = None

    def __init__(self, server_name, database_name):
        self.connection_to_db = pyodbc.connect(r'Driver={SQL Server};Server='+server_name+';Database='+database_name+';Trusted_Connection=yes;')
        self.cursor = self.connection_to_db.cursor()

    def clear_table(self, table_name):
        self.cursor.execute(f'TRUNCATE TABLE {table_name}')
        self.connection_to_db.commit()

    def add_record(self, table_name, values):
        query = f"INSERT INTO dbo.{table_name} (Mark, Model, Year, Link, EngineCapacity, EnginePower, FuelType, Transmission, DriveWheels,Milage, Price, Image, Location) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);"
        self.cursor.execute(query, values)
        self.connection_to_db.commit()



from datebase import DateBase


datebase = DateBase('Autos.db')
first_query = '''CREATE TABLE News(
ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
link NVARCHAR(100) NOT NULL,
title NVARCHAR(300) NOT NULL,
anons NVARCHAR(500),
image NVARCHAR(300),
text TEXT,
tables TEXT,
date DATETIME);
'''

second_query = '''
CREATE TABLE Auto(
   ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
   Mark           NVARCHAR(100) NOT NULL,
   Model            NVARCHAR(100)     NOT NULL,
   Year        INTEGER NOT NULL,
   Link         NVARCHAR(300) NOT NULL,
   EngineCapacity FLOAT,
   EnginePower            INT,
   FuelType        NVARCHAR(50),
   Transmission         NVARCHAR(50),
   DriveWheels NVARCHAR(50),
   Milage         INTEGER,
   Price        INTEGER,
   Image         NVARCHAR(300),
   Location        NVARCHAR(100)
);
'''

queries = [first_query, second_query]

for query in queries:
    datebase.create_table(query)
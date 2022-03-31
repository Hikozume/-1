import pyodbc

name_server = 'SRV2'
databese = 'Base_python'

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+name_server+";"
                                   "Database="+databese+";"
                                   "Trusted_Connection=yes;")

cursor = cnxn.cursor()

insert_query = '''INSERT INTO MarkAndModels (Mark, Model)
                  VALUES (?, ?);'''

file = open('model.txt', 'r')
for line in file:
    res = line.split(';')
    cursor.execute(insert_query, res[0], res[1])
cnxn.commit()

cursor.execute('SELECT TOP 100 * FROM MarkAndModels')

for row in cursor:
    print(row)
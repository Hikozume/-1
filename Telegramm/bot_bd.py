import pyodbc

name_server = 'SRV2'
databese_users = 'Base_python'
database_ads = 'Auto'

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+name_server+";"
                                   "Database="+databese_users+";"
                                   "Trusted_Connection=yes;")

cursor = cnxn.cursor()

cnxn_autos = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server="+name_server+";"
                                   "Database="+database_ads+";"
                                   "Trusted_Connection=yes;")

cursor_auto = cnxn_autos.cursor()

#insert_query = '''INSERT INTO MarkAndModels (Mark, Model) VALUES (?, ?);'''


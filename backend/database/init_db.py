import sqlite3


connection = sqlite3.connect('database.db')

'''
with open('database.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open('populate_db.sql') as f:
    connection.executescript(f.read())

'''

connection.commit()
connection.close()

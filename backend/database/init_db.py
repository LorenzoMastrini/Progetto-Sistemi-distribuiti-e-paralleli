import sqlite3


DB_DIR_ABSOLUTE_PATH = 'C:/Users/lollo/Desktop/Informatics/Programming/Sistemi distribuiti e paralleli/Progetto Sistemi distribuiti e paralleli/backend/database/'

connection = sqlite3.connect('database.db')

with open(DB_DIR_ABSOLUTE_PATH + 'database.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open(DB_DIR_ABSOLUTE_PATH + 'populate_db.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
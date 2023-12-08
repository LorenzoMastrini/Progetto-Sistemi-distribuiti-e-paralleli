import sqlite3


DB_DIR_ABSOLUTE_PATH_RICCARDO = 'C:/Users/rcano/Documents/Uni/SDEP/Progetto-Sistemi-distribuiti-e-paralleli/backend/database/'
DB_DIR_ABSOLUTE_PATH_LORENZO = 'C:/Users/lollo/Desktop/Informatics/Programming/Sistemi distribuiti e paralleli/Progetto Sistemi distribuiti e paralleli/backend/database/'

connection = sqlite3.connect(DB_DIR_ABSOLUTE_PATH_LORENZO + 'database.db')

with open(DB_DIR_ABSOLUTE_PATH_LORENZO + 'database.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

with open(DB_DIR_ABSOLUTE_PATH_LORENZO + 'populate_db.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
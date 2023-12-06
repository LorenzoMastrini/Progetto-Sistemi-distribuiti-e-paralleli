import sqlite3

def connect_to_db():                            #funzione per connettersi
    conn = sqlite3.connect('./database.db')
    return conn

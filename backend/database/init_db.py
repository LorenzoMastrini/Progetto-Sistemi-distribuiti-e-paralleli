import os
import sqlite3

DB_DIR_ABSOLUTE_PATH_RICCARDO = 'C:/Users/rcano/Documents/Uni/SDEP/Progetto-Sistemi-distribuiti-e-paralleli/backend/database/'
DB_DIR_ABSOLUTE_PATH_LORENZO = 'C:/Users/lollo/Desktop/Informatics/Programming/Sistemi distribuiti e paralleli/Progetto Sistemi distribuiti e paralleli/backend/database/'

if(not os.path.exists(DB_DIR_ABSOLUTE_PATH_RICCARDO + 'database.db')):                               
    connection = sqlite3.connect(DB_DIR_ABSOLUTE_PATH_RICCARDO + 'database.db')         #stabilisco una connessione con il database  
    
    with open(DB_DIR_ABSOLUTE_PATH_RICCARDO + 'database.sql') as f:                      
        connection.executescript(f.read())                                             #eseguo lo script "database.sql" per la creazione delle tabelle

    cur = connection.cursor()

    with open(DB_DIR_ABSOLUTE_PATH_RICCARDO + 'populate_db.sql') as f:                  #eseguo lo script "populate_db.sql" per l'inserimento di dati di esempio nel DB
        connection.executescript(f.read())

    connection.commit()                                                                #salvo le modifiche fatte al DB
    connection.close()                                                                 #chiudo la connessione

def connect_to_db():                                                                   #funzione per connettersi
    conn = sqlite3.connect('./backend/database/database.db')
    return conn
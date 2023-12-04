import sqlite3

def connect_to_db():                            #funzione per connettersi
    conn = sqlite3.connect('./database.db')
    return conn

def init_db_table():                            #funzione per inizializzare il DB creando le tabelle necessarie
    try:
        conn = connect_to_db()

        conn.execute('DROP TABLE IF EXISTS film;')
        conn.execute('DROP TABLE IF EXISTS room;')
        conn.execute('DROP TABLE IF EXISTS schedule;')
        
        conn.execute('''
            CREATE TABLE film (
                name VARCHAR(255) PRIMARY KEY NOT NULL,
                duration INTEGER NOT NULL,
                plot VARCHAR(512) NOT NULL,
                director VARCHAR(255) NOT NULL
            ); 
        ''')

        conn.execute('''
            CREATE TABLE room (
                id INTEGER PRIMARY KEY NOT NULL,
                n_seats INTEGER NOT NULL
            );
        ''')
        
        conn.execute('''
            CREATE TABLE schedule (
                time TEXT NOT NULL,
                room_id INTEGER NOT NULL REFERENCES room(id),
                film VARCHAR(255) REFERENCES film(name), 
                seats_available INTEGER,
                    
                PRIMARY KEY (time, room_id)
            );
        ''')

        conn.commit()
        print('Tables created successfully')

    finally:
        conn.close()



init_db_table()

conn = connect_to_db()
conn.executescript('''
    INSERT INTO room VALUES (1, 100);

    INSERT INTO film VALUES ("Interstellar", 140, "cuofdjsfnrsuifksb", "Christopher Nolan");
    INSERT INTO film VALUES ("Pulp Fiction", 125, "fdafeawr", "Quentin Tarantino");
    INSERT INTO film VALUES ("The VVitch", 120, "aiutoooooooo", "Robert Eggers");

    INSERT INTO schedule VALUES (datetime("2023-12-02 21:00"), 1, "The VVitch", NULL);                  
    INSERT INTO schedule VALUES (datetime("2023-12-02 23:00"), 1, "The VVitch", NULL);
    INSERT INTO schedule VALUES (datetime("2023-12-03 16:00"), 1, "Interstellar", NULL);
    INSERT INTO schedule VALUES (datetime("2023-12-03 19:00"), 1, "Pulp Fiction", NULL);
    INSERT INTO schedule VALUES (datetime("2023-12-04 18:00"), 1, "Pulp Fiction", NULL);
    UPDATE schedule SET seats_available = (SELECT room.n_seats FROM room INNER JOIN schedule ON room.id = schedule.room_id)
''')
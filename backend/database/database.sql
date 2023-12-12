DROP TABLE IF EXISTS film;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS users;

CREATE TABLE film (
    name VARCHAR(255) PRIMARY KEY NOT NULL,
    duration INTEGER NOT NULL,
    plot VARCHAR(512) NOT NULL,
    director VARCHAR(255) NOT NULL
);

CREATE TABLE room (
    id INTEGER PRIMARY KEY NOT NULL,
    n_seats INTEGER NOT NULL
);

CREATE TABLE schedule (
    movie_time TEXT NOT NULL,
    room_id INTEGER NOT NULL REFERENCES room(id),
    film VARCHAR(255) REFERENCES film(name), 
    seats_available INTEGER,
                    
    PRIMARY KEY (movie_time, room_id)
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOL NOT NULL DEFAULT false
);
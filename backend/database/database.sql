DROP TABLE IF EXISTS film;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS reservation;

CREATE TABLE film (
    name VARCHAR(255) PRIMARY KEY NOT NULL,
    duration INTEGER NOT NULL,
    plot VARCHAR(512) NOT NULL,
    director VARCHAR(255) NOT NULL
);

CREATE TABLE schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
    movie_time TEXT NOT NULL,
    film VARCHAR(255) REFERENCES film(name), 
    seats_available INTEGER DEFAULT 100                
);

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE reservation (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    movie_time TEXT NOT NULL REFERENCES schedule(movie_time),
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    n_seats INTEGER NOT NULL
);
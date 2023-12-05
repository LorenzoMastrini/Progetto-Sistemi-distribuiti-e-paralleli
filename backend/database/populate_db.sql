INSERT INTO room VALUES (1, 100);

INSERT INTO film VALUES ("Interstellar", 140, "cuofdjsfnrsuifksb", "Christopher Nolan");
INSERT INTO film VALUES ("Pulp Fiction", 125, "fdafeawr", "Quentin Tarantino");
INSERT INTO film VALUES ("The VVitch", 120, "aiutoooooooo", "Robert Eggers");

INSERT INTO schedule VALUES (datetime("2023-12-02 21:00"), 1, "The VVitch", NULL);                  
INSERT INTO schedule VALUES (datetime("2023-12-02 23:00"), 1, "The VVitch", NULL);
INSERT INTO schedule VALUES (datetime("2023-12-03 16:00"), 1, "Interstellar", NULL);
INSERT INTO schedule VALUES (datetime("2023-12-03 19:00"), 1, "Pulp Fiction", NULL);
INSERT INTO schedule VALUES (datetime("2023-12-04 18:00"), 1, "Pulp Fiction", NULL);

INSERT INTO users VALUES (1, "Jesus", "iosonogesu@gmail.com", "culo1", true);
INSERT INTO users VALUES (2, "Even Flow", "even.flow@gmail.com", "culo2", false);

UPDATE schedule SET seats_available = (SELECT room.n_seats FROM room INNER JOIN schedule ON room.id = schedule.room_id)
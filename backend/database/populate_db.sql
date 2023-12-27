INSERT INTO film VALUES ("Interstellar", 140, "cuofdjsfnrsuifksb", "Christopher Nolan", "assets/film-1.jpg");
INSERT INTO film VALUES ("Pulp Fiction", 125, "fdafeawr", "Quentin Tarantino", "assets/film-2.jpg");
INSERT INTO film VALUES ("The VVitch", 120, "aiutoooooooo", "Robert Eggers", "assets/film-3.jpg");

INSERT INTO schedule (movie_time, film) VALUES (datetime("2023-12-02 21:00"), "The VVitch");                  
INSERT INTO schedule (movie_time, film) VALUES (datetime("2023-12-02 23:00"), "The VVitch");
INSERT INTO schedule (movie_time, film) VALUES (datetime("2023-12-03 16:00"), "Interstellar");
INSERT INTO schedule (movie_time, film) VALUES (datetime("2023-12-03 19:00"), "Pulp Fiction");
INSERT INTO schedule (movie_time, film) VALUES (datetime("2023-12-04 18:00"), "Pulp Fiction");

INSERT INTO users VALUES (NULL, "Jesus", "iosonogesu@gmail.com", "b4bcfc658cfc5e3bcabbbec8218d7a421b8b963ec36bf181b72ffabc03fccdf0", true, NULL);
INSERT INTO users VALUES (NULL, "Even Flow", "even.flow@gmail.com", "d1c1e52efdc0a5d5ddeb29239bfa99b36c2de09aad2b7a484b30c2120a37ef5c", false, NULL);

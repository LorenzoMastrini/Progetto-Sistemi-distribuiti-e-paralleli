INSERT INTO film VALUES ("Interstellar", 169, "Una squadra di esploratori viaggia attraverso un wormhole nello spazio nel tentativo di assicurare la sopravvivenza dell'umanità.", "Christopher Nolan", "assets/film-1.jpg", "Avventura, Drammatico, Sci-Fi");
INSERT INTO film VALUES ("Pulp Fiction", 154, "Le vite di due sicari, un pugile, un gangster e sua moglie, e una coppia di banditi in un diner si intrecciano in quattro storie di violenza e redenzione.", "Quentin Tarantino", "assets/film-2.jpg", "Crimine, Drammatico");
INSERT INTO film VALUES ("The VVitch", 92, "Una famiglia nel New England del 1630 viene fatta a pezzi dalle forze della stregoneria, della magia nera e della possessione.", "Robert Eggers", "assets/film-3.jpg", "Drammatico, Fantasy, Horror, Mistero, Thriller");
INSERT INTO film VALUES ("Alien", 117, "L'equipaggio di una nave spaziale commerciale incontra una specie aliena letale dopo la ricezione di una trasmissione sconosciuta.", "Ridley Scott", "assets/film-5.jpg", "Horror, Sci-Fi");

INSERT INTO schedule (movie_time, film) VALUES (datetime("2024-01-16 21:00:00"), "Alien");                  
INSERT INTO schedule (movie_time, film) VALUES (datetime("2024-01-16 18:00:00"), "Pulp Fiction");
INSERT INTO schedule (movie_time, film) VALUES (datetime("2024-01-17 20:30:00"), "Interstellar");
INSERT INTO schedule (movie_time, film) VALUES (datetime("2024-01-17 18:00:00"), "Alien");
INSERT INTO schedule (movie_time, film) VALUES (datetime("2024-01-16 22:45:00"), "The VVitch");

INSERT INTO users VALUES (NULL, "Vincent", "vincent@gmail.com", "5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5", true, NULL);
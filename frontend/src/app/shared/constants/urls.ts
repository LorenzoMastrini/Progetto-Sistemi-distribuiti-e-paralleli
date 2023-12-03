//gestisco tutti gli urls da un'unico file
const BASE_URL = 'http://localhost:5000'; //url base del server, condiviso da tutte le APIs

export const FILMS_URL = BASE_URL + '/api/films'; //url per ottenere tutti i film
export const FILMS_GENRES_URL = FILMS_URL + '/genres'; //url per ottenere tutti i generi
export const FILMS_BY_SEARCH_URL = FILMS_URL + '/search/'; //url per ottenere i film in base alla ricerca ('/' alla fine sarà seguito dal searchTerm)
export const FILMS_BY_GENRE_URL = FILMS_URL + '/genre/'; //url per ottenere i film in base al genere ('/' alla fine sarà seguito dal genere)
export const FILMS_BY_ID_URL = FILMS_URL + '/'; //url per ottenere i film in base all'id ('/' alla fine sarà seguito dall'id)

export const USER_LOGIN_URL = BASE_URL + '/api/users/login'; //url per la pagina di login
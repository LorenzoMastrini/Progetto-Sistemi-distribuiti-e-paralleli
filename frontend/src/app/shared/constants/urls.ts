//gestisco tutti gli urls da un'unico file
const BASE_URL = 'http://localhost:5000'; //url base del server, condiviso da tutte le APIs

export const FILMS_URL = BASE_URL + '/api/films'; //url per ottenere tutti i film
export const FILMS_BY_NAME_URL = FILMS_URL + '/'; //url per ottenere i film in base al nome ('/' alla fine sarà seguito dal nome)

export const SCHEDULE_FILM_URL = BASE_URL + '/api/schedule/'; //url per ottenere i film in base all'id ('/' alla fine sarà seguito dall'id)

export const USER_LOGIN_URL = BASE_URL + '/api/users/login'; //url per la pagina di login
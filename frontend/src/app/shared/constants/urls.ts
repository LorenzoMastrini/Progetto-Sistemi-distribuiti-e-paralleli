//gestisco tutti gli urls da un'unico file
const BASE_URL = 'http://localhost:5000'; //url base del server, condiviso da tutte le APIs

export const FILMS_URL = BASE_URL + '/api/films'; //url per ottenere tutti i film
export const FILMS_BY_NAME_URL = FILMS_URL + '/'; //url per ottenere i film in base al nome ('/' alla fine sarà seguito dal nome)
export const SCHEDULE_FILM_URL = FILMS_URL + '/schedule/'; //url per ottenere i film in base all'id ('/' alla fine sarà seguito dall'id)
export const BOOK_TICKETS_URL = FILMS_URL + '/reserve'; //url per prenotare biglietti per l'orario di un film

export const USER_URL = BASE_URL + '/api/users';
export const USER_LOGIN_URL = USER_URL + '/login'; //url per l'api del login
export const USER_REGISTER_URL = USER_URL + '/registration'; //url per l'api della registrazione di nuovi utenti
export const USER_ORDERS_URL = USER_URL + '/orders/'; //url per l'api della registrazione di nuovi utenti

export const ADMIN_URL = BASE_URL + '/api/admin';
export const ADMIN_GET_ALL_SCHEDULES = ADMIN_URL + '/films/schedule/get-schedules';
export const ADMIN_ADD_FILM = ADMIN_URL + '/films/add-film';
export const ADMIN_ADD_SCHEDULE = ADMIN_URL + '/films/schedule/add-schedule';
export const ADMIN_GET_ALL_USERS = ADMIN_URL + '/users';
export const ADMIN_CHANGE_ADMIN_STATUS = ADMIN_URL + '/users/change-admin/';
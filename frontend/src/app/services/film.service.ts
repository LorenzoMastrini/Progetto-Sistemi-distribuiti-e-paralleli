import { Injectable } from '@angular/core';
import { Film } from '../shared/models/Film';
import { HttpClient } from '@angular/common/http';
import { BOOK_TICKETS_URL, FILMS_BY_NAME_URL, FILMS_URL, SCHEDULE_FILM_URL } from '../shared/constants/urls';
import { Observable } from 'rxjs';
import { Schedule } from '../shared/models/Schedule';
import { BookingInfo } from '../shared/models/BookingInfo';

@Injectable({
  providedIn: 'root'
})

export class FilmService {
  constructor(private http:HttpClient) { }

  //l'HttpClient non invierà i dati raw di tipo 'Film' ma un Observable su cui devo fare subscribe;
  //dopo che la connessione al backend sarà finita, questo fornirà i dati o tornerà un errore
  getAll(): Observable<Film[]> {
    return this.http.get<Film[]>(FILMS_URL);
  }

  getFilmByName(filmName: string): Observable<Film> {
    return this.http.get<Film>(FILMS_BY_NAME_URL + filmName);
  }

  getFilmSchedule(filmName: string): Observable<Schedule[]> {
    return this.http.get<Schedule[]>(SCHEDULE_FILM_URL + filmName);
  }

  reserve(bookingInfo: BookingInfo): Observable<BookingInfo> {
    return this.http.post<BookingInfo>(BOOK_TICKETS_URL, bookingInfo);
  }
}

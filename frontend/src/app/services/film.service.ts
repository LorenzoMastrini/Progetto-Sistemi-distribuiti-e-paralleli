import { Injectable } from '@angular/core';
import { Film } from '../shared/models/Film';
import { HttpClient } from '@angular/common/http';
import { FILMS_BY_ID_URL, FILMS_URL } from '../shared/constants/urls';
import { Observable } from 'rxjs';

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

  getFilmById(filmId: string): Observable<Film> {
    return this.http.get<Film>(FILMS_BY_ID_URL + filmId);
  }
}

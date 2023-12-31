import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { FilmService } from 'src/app/services/film.service';
import { Film } from 'src/app/shared/models/Film';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent {
  films: Film[] = []; //mantiene i dati che otteniamo da FilmService

  constructor(filmService: FilmService, activatedRoute: ActivatedRoute) {
    let filmsObservable: Observable<Film[]>; //per ottere gli observable di tutti i metodi chiamati che si connettono al backend, poi facendo subscribe per ottere i film
    //altrimenti dovrei fare subscribe per ognuno dei metodi chiamati separatamente
    
    activatedRoute.params.subscribe(_ => {
      filmsObservable = filmService.getAll(); //mostra tutti i film

      filmsObservable.subscribe((serverFilms) => {
        this.films = serverFilms;
      });
    });
  }
}

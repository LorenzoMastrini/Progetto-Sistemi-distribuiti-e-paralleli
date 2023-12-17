import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { AdminService } from 'src/app/services/admin.service';
import { FilmService } from 'src/app/services/film.service';
import { Film } from 'src/app/shared/models/Film';
import { Schedule } from 'src/app/shared/models/Schedule';

@Component({
  selector: 'app-admin-home',
  templateUrl: './admin-home.component.html',
  styleUrls: ['./admin-home.component.css']
})

export class AdminHomeComponent {
  films: Film[] = [];
  schedules: Schedule[] = [];

  constructor(filmService: FilmService, activatedRoute: ActivatedRoute, private adminService:AdminService) {
    let filmsObservable: Observable<Film[]>; //per ottere gli observable di tutti i metodi chiamati che si connettono al backend, poi facendo subscribe per ottere i film
    //altrimenti dovrei fare subscribe per ognuno dei metodi chiamati separatamente
    
    //ogni volta che 'params' cambia, chiama la funzione dentro 'subscribe()'
    activatedRoute.params.subscribe(() => {
      filmsObservable = filmService.getAll(); //se non è stato cercato nulla mostra tutto per default

      filmsObservable.subscribe((serverFilms) => {
        this.films = serverFilms;
      });
    });

    let schedulesObservable: Observable<Schedule[]>; //per ottere gli observable di tutti i metodi chiamati che si connettono al backend, poi facendo subscribe per ottere i film
    //altrimenti dovrei fare subscribe per ognuno dei metodi chiamati separatamente
    
    //ogni volta che 'params' cambia, chiama la funzione dentro 'subscribe()'
    activatedRoute.params.subscribe(() => {
      schedulesObservable = adminService.getAllSchedules(); //se non è stato cercato nulla mostra tutto per default

      schedulesObservable.subscribe((serverSchedules) => {
        this.schedules = serverSchedules;
      });
    });
  }
}
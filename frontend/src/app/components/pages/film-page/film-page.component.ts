import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FilmService } from 'src/app/services/film.service';
import { Film } from 'src/app/shared/models/Film';
import { Schedule } from 'src/app/shared/models/Schedule';

@Component({
  selector: 'app-film-page',
  templateUrl: './film-page.component.html',
  styleUrls: ['./film-page.component.css']
})

export class FilmPageComponent {
  film!: Film;
  schedule?: Schedule[];
  totalPrice?: number;

  constructor(activatedRoute:ActivatedRoute, filmService:FilmService, private router:Router) {
    activatedRoute.params.subscribe((params) => {
      if(params.name) {
        filmService.getFilmByName(params.name).subscribe(serverFilm => {
          this.film = serverFilm;
          
          filmService.getFilmSchedule(params.name).subscribe(serverFilmSchedule => {
            this.schedule = serverFilmSchedule;
          });
        });
      }
    });
  }

  changeRentDays(film:Film, nTicketsInString:string) {
    const nTickets = parseInt(nTicketsInString);
    film.price = 1;
    this.totalPrice = film.price * nTickets;
  }

  bookTickets() {
    
  }
}

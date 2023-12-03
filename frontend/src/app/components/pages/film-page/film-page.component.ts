import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CartService } from 'src/app/services/cart.service';
import { FilmService } from 'src/app/services/film.service';
import { Film } from 'src/app/shared/models/Film';

@Component({
  selector: 'app-film-page',
  templateUrl: './film-page.component.html',
  styleUrls: ['./film-page.component.css']
})

export class FilmPageComponent {
  film!: Film;

  constructor(activatedRoute:ActivatedRoute, filmService:FilmService, private cartService:CartService, private router:Router) {
    activatedRoute.params.subscribe((params) => {
      if(params.id) {
        filmService.getFilmById(params.name).subscribe(serverFilm => {
          serverFilm = JSON.parse(JSON.stringify(serverFilm));
          this.film = serverFilm;
          
          console.log(this.film);
        });
      }
    });
  }

  addToCart() {
    this.cartService.addToCart(this.film);
    this.router.navigateByUrl('/cart-page');
  }
}

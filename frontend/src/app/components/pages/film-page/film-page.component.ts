import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { FilmService } from 'src/app/services/film.service';
import { UserService } from 'src/app/services/user.service';
import { FILMS_PRICE_PER_TICKET } from 'src/app/shared/constants/constants';
import { BookingInfo } from 'src/app/shared/models/BookingInfo';
import { Film } from 'src/app/shared/models/Film';
import { Schedule } from 'src/app/shared/models/Schedule';

@Component({
  selector: 'app-film-page',
  templateUrl: './film-page.component.html',
  styleUrls: ['./film-page.component.css']
})

export class FilmPageComponent implements OnInit {
  pricePerTicket = FILMS_PRICE_PER_TICKET;
  film!: Film;
  schedules!: Schedule[]; //lista degli orari disponibili per il film selezionato
  totalPrice?: number; //prezzo per ogni biglietto, poi moltiplicato per il numero di biglietti prenotati
  bookingForm!: FormGroup;
  isSubmitted = false;
  maxBookableTickets: number[] = []; //si possono prenotare al massimo 10 biglietti (se almeno 10 posti sono disponibili)
  scheduleIndex!: number; //valore letto dall'html dinamicamente in base all'orario selezionato dall'utente (poi usato per verificare i posti disponibili)

  constructor(activatedRoute:ActivatedRoute,
              private filmService:FilmService,
              private router:Router,
              private formBuilder:FormBuilder,
              private userService:UserService) {
    activatedRoute.params.subscribe((params) => {
      if(params.name) {
        filmService.getFilmByName(params.name).subscribe(serverFilm => {
          this.film = serverFilm;

          filmService.getFilmSchedule(params.name).subscribe(serverFilmSchedule => {
            this.schedules = serverFilmSchedule;
          });
        });
      }
    });
  }

  ngOnInit(): void {
    this.bookingForm = this.formBuilder.group({
      movieTimeRadio: new FormControl('', Validators.required),
      nTickets: new FormControl('', Validators.required)
    });
  }

  //funzione chiamata quando l'utente cambia l'orario del film tramite radio button
  checkAvailableSeats() {
    let selectedSchedule = this.schedules[this.scheduleIndex]; //orario selezionato tramite radio button

    //se i posti disponibili sono meno del massimo numero prenotabile, ne fa prenotare meno (cioè al massimo il numero di posti disponibili)
    if(selectedSchedule.seatsAvailable < 10 ) {
      this.maxBookableTickets = [];

      for(let i = 1; i <= selectedSchedule.seatsAvailable; i++) {
        this.maxBookableTickets.push(i); //riempie l'array fino al massimo numero di posti disponibili
      }
    } else {
      this.maxBookableTickets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; //altrimenti considera il limite globale di prenotazione biglietti
    }
  }

  changeNumberOfTickets(nTicketsInString:string) {
    const nTickets = parseInt(nTicketsInString);
    this.totalPrice = FILMS_PRICE_PER_TICKET * nTickets;
  }

  bookTickets(nTickets: string) {
    const bookingInfo = new BookingInfo();
    bookingInfo["filmName"] = this.film.name;
    bookingInfo["movieTime"] = this.schedules[this.scheduleIndex].movieTime;
    bookingInfo["roomId"] = this.schedules[this.scheduleIndex].roomId;
    bookingInfo["nSeats"] = parseInt(nTickets);
    bookingInfo["userId"] = parseInt(this.userService.currentUser.id);

    console.log(bookingInfo);
    this.filmService.reserve(bookingInfo).subscribe(() => {
      //torna all'url precedente se il login avviene con successo  
      //this.router.navigateByUrl('/orders');
    });;
  }
}
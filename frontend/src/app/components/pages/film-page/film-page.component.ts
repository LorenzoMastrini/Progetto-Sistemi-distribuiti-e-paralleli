import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { FilmService } from 'src/app/services/film.service';
import { OrderService } from 'src/app/services/order.service';
import { UserService } from 'src/app/services/user.service';
import { FILMS_PRICE_PER_TICKET } from 'src/app/shared/constants/constants';
import { Film } from 'src/app/shared/models/Film';
import { Order } from 'src/app/shared/models/Order';
import { Schedule } from 'src/app/shared/models/Schedule';

@Component({
  selector: 'app-film-page',
  templateUrl: './film-page.component.html',
  styleUrls: ['./film-page.component.css']
})

export class FilmPageComponent implements OnInit {
  film!: Film;
  schedules!: Schedule[]; //lista degli orari disponibili per il film selezionato
  totalPrice!: number; //prezzo per ogni biglietto, poi moltiplicato per il numero di biglietti prenotati
  bookingForm!: FormGroup;
  isSubmitted = false;
  maxBookableTickets: number[] = []; //si possono prenotare al massimo 10 biglietti (se almeno 10 posti sono disponibili)
  scheduleIndex!: number; //valore letto dall'HTML dinamicamente in base all'orario selezionato dall'utente (poi usato per verificare i posti disponibili)
  radioButtonIsSelected: boolean = false; //per aggiornare dinamicamente il template HTML con la parte dedicata alla prenotazione
  availableSeats: string[] | undefined;
  
  constructor(activatedRoute:ActivatedRoute,
              filmService:FilmService,
              private orderService:OrderService,
              private router:Router,
              private formBuilder:FormBuilder,
              private userService:UserService) {
    activatedRoute.params.subscribe((params) => {
      if(params.name) { //parametro preso dall'url (.../fim/nomeFilm)
        filmService.getFilmByName(params.name).subscribe(serverFilm => {
          this.film = serverFilm;

          //richiede anche tutta la programmazione del film nel database
          filmService.getFilmSchedule(params.name).subscribe(serverFilmSchedule => {
            this.schedules = serverFilmSchedule;
          });
        });
      }
    });
  }

  ngOnInit(): void {
    //form per la prenotazione dei posti
    this.bookingForm = this.formBuilder.group({
      movieTimeRadio: new FormControl('', Validators.required),
      nTickets: new FormControl('', Validators.required)
    });
  }

  //torna la lista di posti disponibili per un certo orario
  getSeatsOfSpecificSchedule(): string[] | undefined {
    //trova l'orario dinamicamente in base a quale radio button ha selezionato l'utente
    let selectedTime: string = (document.querySelector('input[type=radio]:checked') as HTMLInputElement).id;
    return this.schedules.find(schedule => schedule.movieTime == selectedTime)?.seatsAvailable;
  }

  //funzione chiamata quando l'utente cambia l'orario del film tramite radio button
  checkAvailableSeats() {
    this.radioButtonIsSelected = true;
    this.availableSeats = this.getSeatsOfSpecificSchedule();
    let selectedSchedule = this.schedules[this.scheduleIndex]; //orario selezionato tramite radio button

    //se i posti disponibili sono meno del massimo numero prenotabile, ne fa prenotare meno (cioè al massimo il numero di posti disponibili)
    if(selectedSchedule.seatsAvailable.length < 10 ) {
      this.maxBookableTickets = [];

      for(let i = 1; i <= selectedSchedule.seatsAvailable.length; i++) {
        this.maxBookableTickets.push(i); //riempie l'array fino al massimo numero di posti disponibili
      }
    } else {
      this.maxBookableTickets = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]; //altrimenti considera il limite globale di prenotazione biglietti
    }
  }

  changeNumberOfTickets(nTicketsInString:string) {
    const nTickets = parseInt(nTicketsInString); //numero di posti che si vogliono prenotare
    this.totalPrice = FILMS_PRICE_PER_TICKET * nTickets; //calcolo del costo totale in base al numero di posti
  }

  //funzione per controllare se i posti scelti dall'utente corrispondono col valore di biglietti che vuole prenotare
  checkSeats(e: Event, nSelectedTicketsInString: string) {
    if(document.querySelectorAll('input[type=checkbox]:checked').length > parseInt(nSelectedTicketsInString)) {
      alert("Numero di posti massimo raggiunto");
      (e.target as HTMLInputElement).checked = false; //reimposta a false l'ultima checkbox selezionata (cioè annulla la selezione del posto)
    }
  }

  createOrder(nTickets: string) {
    //serve essere autenticati per prenotare i posti
    if(this.userService.currentUser.id == undefined) {
      this.router.navigateByUrl('/login');
      return;
    }

    //arrivo qua solo se l'utente ha effettuato il login
    let bookedSeats = []; //variabile per salvare i posti che l'utente ha scelto
    let checkboxes = document.querySelectorAll('input[type=checkbox]:checked'); //lista delle checkbox corrispondenti ai posti scelti

    if(parseInt(nTickets) !== checkboxes.length) {
      alert("Il numero di biglietti scelto e i posti selezionati non corrispondono");
      return;
    }

    //riempe l'array con i posti
    for(let i = 0; i < checkboxes.length; i++) {
      bookedSeats.push((checkboxes[i] as HTMLInputElement).value);
    }

    const newOrder = new Order();
    newOrder["movieTime"] = this.schedules[this.scheduleIndex].movieTime;
    newOrder["seats"] = bookedSeats;
    newOrder["userId"] = parseInt(this.userService.currentUser.id);
    newOrder["totalPrice"] = this.totalPrice;

    this.orderService.createOrder(newOrder);
    this.router.navigateByUrl('/payment');
  }

  get pricePerTicket() {
    return FILMS_PRICE_PER_TICKET; //deve essere letto nell'HTML, non fattibile con la costante importata dal file constants.ts
  }
}
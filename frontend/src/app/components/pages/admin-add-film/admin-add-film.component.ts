import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AdminService } from 'src/app/services/admin.service';
import { Film } from 'src/app/shared/models/Film';

@Component({
  selector: 'app-admin-add-film',
  templateUrl: './admin-add-film.component.html',
  styleUrls: ['./admin-add-film.component.css']
})

export class AdminAddFilmComponent {
  addFilmForm!: FormGroup; //form per inviare i dati
  isSubmitted = false; //per indicare se l'utente ha premuto o meno il pulsante per il submit, per non mostrare subito gli errori di validazione dei dati

  constructor(private formBuilder:FormBuilder,
              private adminService:AdminService,
              private router:Router) { }

  ngOnInit(): void {
    //tramite formBuilder creo il form group per i vari campi che l'utente dovrà compilare
    this.addFilmForm = this.formBuilder.group({
      //qui definisco tutti gli input e i loro validators 
      //il primo valore di entrambi è il valore di default, e il secondo sono i validators
      name: ['', Validators.required],
      duration: ['', Validators.required],
      genres: ['', Validators.required],
      director: ['', Validators.required],
      plot: ['', Validators.required],
      imgUrl: ['', Validators.required]
    });
  }

  //solo per accorciare le chiamate nell'html: fc.email al posto di loginForm.controls.email
  get fc() {
    return this.addFilmForm.controls;
  }

  submit() {
    this.isSubmitted = true;

    console.log("prova fuori");

    if(this.addFilmForm.invalid) {
      return; //torna se il form non è valido
    }

    this.adminService.addFilm({
                                name: this.fc.name.value,
                                duration: parseInt(this.fc.duration.value),
                                genres: this.fc.genres.value,
                                director: this.fc.director.value,
                                plot: this.fc.plot.value,
                                imgUrl: this.fc.imgUrl.value
    }).subscribe((serverNewFilm) => {
      //NON LO TORNA NON SO COME MAI (forse non necessario)
      let prova: Film = serverNewFilm;
      //console.log(prova);
      console.log("prova dentro");
    });

    this.router.navigateByUrl("/admin"); //torna alla home dell'admin
  }
}

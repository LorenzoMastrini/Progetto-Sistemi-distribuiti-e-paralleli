import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { AbstractControl } from '@angular/forms';

const VALIDATORS_MESSAGES: any = {
  required: 'Il campo non può essere vuoto',
  email: 'Email non valida'
}

@Component({
  selector: 'input-validation',
  templateUrl: './input-validation.component.html',
  styleUrls: ['./input-validation.component.css']
})

export class InputValidationComponent implements OnInit, OnChanges {
  @Input()
  control!: AbstractControl;
  @Input()
  showErrorsWhen: boolean = true;
  errorMessages: string[] = []; //verrà riempito in base ai controlli a tempo di esecuzione

  ngOnInit(): void {
    //quando cambia lo stato della validazione
    this.control.statusChanges.subscribe(() => {
      this.checkValidation();
    });

    //quando cambia il valore, cioè viene immesso qualcosa nella casella di input
    this.control.valueChanges.subscribe(() => {
      this.checkValidation();
    });
  }

  //chiamato ad ogni cambiamento del componente
  ngOnChanges(changes: SimpleChanges): void {
    this.checkValidation();
  }

  //riempe la variabile errorMessages
  checkValidation(): void {
    const errors = this.control.errors;
    
    if(!errors) { //non ci sono errori
      this.errorMessages = [];
      return
    }

    const errorKeys = Object.keys(errors); //ritorna un array di chiavi per ogni errore, per mapparle con le rispettive stringhe da mostrare
    this.errorMessages = errorKeys.map(key => VALIDATORS_MESSAGES[key]); //questo alla fine è un array di errori (le stringhe da mostrare all'utente)
  }
}

import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AdminService } from 'src/app/services/admin.service';
import { Schedule } from 'src/app/shared/models/Schedule';

@Component({
  selector: 'app-admin-add-schedule',
  templateUrl: './admin-add-schedule.component.html',
  styleUrls: ['./admin-add-schedule.component.css']
})
export class AdminAddScheduleComponent {
  addScheduleForm!: FormGroup; //form per inviare i dati
  isSubmitted = false; //per indicare se l'utente ha premuto o meno il pulsante per il submit, per non mostrare subito gli errori di validazione dei dati

  constructor(private formBuilder:FormBuilder, private adminService:AdminService) { }

  ngOnInit(): void {
    //tramite formBuilder creo il form group per i vari campi che l'utente dovrà compilare
    this.addScheduleForm = this.formBuilder.group({
      //qui definisco tutti gli input e i loro validators 
      //il primo valore di entrambi è il valore di default, e il secondo sono i validators
      scheduleFilm: ['', Validators.required],
      scheduleTime: ['', Validators.required]
    });
  }

  //solo per accorciare le chiamate nell'html: fc.email al posto di loginForm.controls.email
  get fc() {
    return this.addScheduleForm.controls;
  }

  submit() {
    this.isSubmitted = true;
    console.log("ciao");
    if(this.addScheduleForm.invalid) {
      return; //torna se il form non è valido
    }

    this.adminService.addSchedule({film: this.fc.scheduleFilm.value, movieTime: this.fc.scheduleTime.value}).subscribe((serverNewSchedule) => {
      let prova: Schedule = serverNewSchedule;
      console.log(prova);
    });
  }
}
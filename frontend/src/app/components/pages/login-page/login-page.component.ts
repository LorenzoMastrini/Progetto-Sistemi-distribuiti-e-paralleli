import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.css']
})

export class LoginPageComponent implements OnInit {
  loginForm!: FormGroup; //form per inviare i dati
  isSubmitted = false; //per indicare se l'utente ha premuto o meno il pulsante per il submit, per non mostrare subito gli errori di validazione dei dati
  returnUrl = ''; //fa tornare l'utente alla pagina dove si trovava prima del login

  constructor(private formBuilder:FormBuilder, private userService:UserService,
    private activatedRoute:ActivatedRoute, private router:Router) { }

  ngOnInit(): void {
    //tramite formBuilder creo il form group per i vari campi che l'utente dovrà compilare
    this.loginForm = this.formBuilder.group({
      //qui definisco tutti gli input e i loro validators 
      //il primo valore di entrambi è il valore di default, e il secondo sono i validators
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    //snapshot fornisce l'ultimo valore di activatedRoute, senza bisogno di subscribe()
    this.returnUrl = this.activatedRoute.snapshot.queryParams.returnUrl //queryParams è tutto quello dopo il ? nell'url (in questo caso prende returnUrl)
  }

  //solo per accorciare le chiamate nell'html: fc.email al posto di loginForm.controls.email
  get fc() {
    return this.loginForm.controls;
  }

  submit() {
    this.isSubmitted = true;
    if(this.loginForm.invalid) {
      return; //torna se il form non è valido
    }
  
    this.userService.login({email: this.fc.email.value, password: this.fc.password.value}).subscribe(() => {
        //torna all'url precedente se il login avviene con successo  
        this.router.navigateByUrl(this.returnUrl);
      });
  }
}

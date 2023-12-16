import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { OrderService } from 'src/app/services/order.service';
import { UserService } from 'src/app/services/user.service';
import { Order } from 'src/app/shared/models/Order';

@Component({
  selector: 'app-payment-page',
  templateUrl: './payment-page.component.html',
  styleUrls: ['./payment-page.component.css']
})

export class PaymentPageComponent implements OnInit {
  paymentForm!: FormGroup;

  constructor(private formBuilder:FormBuilder,
              private userService:UserService,
              private toastrService:ToastrService,
              private router:Router,
              private orderService:OrderService) { }

  ngOnInit(): void {
    let {name} = this.userService.currentUser;
    this.paymentForm = this.formBuilder.group({
      name: [name, Validators.required]
    });
  }

  get fc() {
    return this.paymentForm.controls;
  }

  bookTickets() {
    if(this.paymentForm.invalid) {
      this.toastrService.warning("Si prega di compilare i campi obbligatori.", "Input non validi");
      return;
    }

    if(this.userService.currentUser.id == undefined) {
      this.router.navigateByUrl('/login');
      return; //serve essere autenticati per prenotare i posti
    }

    this.orderService.reserve().subscribe(() => {
      //redirige l'utente alla pagina degli ordini
      this.router.navigateByUrl('/');
    });
  }
}

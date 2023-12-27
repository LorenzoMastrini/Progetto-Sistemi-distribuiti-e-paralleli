import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { OrderService } from 'src/app/services/order.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-payment-page',
  templateUrl: './payment-page.component.html',
  styleUrls: ['./payment-page.component.css']
})

export class PaymentPageComponent implements OnInit {
  paymentForm!: FormGroup;
  totalPrice!: number;
  isSubmitted = false;

  constructor(private formBuilder:FormBuilder,
              private userService:UserService,
              private toastrService:ToastrService,
              private router:Router,
              private orderService:OrderService) { }

  ngOnInit(): void {
    this.paymentForm = this.formBuilder.group({
      name: ['', Validators.required],
      surname: ['', Validators.required],
      cardNumber: ['', Validators.required],
      expireDate: ['', Validators.required],
      cvv: ['', Validators.required]
    });

    this.orderService.getOrderObservable().subscribe((order) => {
      this.totalPrice = order.totalPrice;
    });
  }

  get fc() {
    return this.paymentForm.controls;
  }

  bookTickets() {
    this.isSubmitted = true;

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

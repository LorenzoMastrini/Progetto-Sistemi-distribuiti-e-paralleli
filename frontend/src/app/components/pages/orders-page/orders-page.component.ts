import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { FilmService } from 'src/app/services/film.service';
import { OrderService } from 'src/app/services/order.service';
import { UserService } from 'src/app/services/user.service';
import { Order } from 'src/app/shared/models/Order';

@Component({
  selector: 'app-orders-page',
  templateUrl: './orders-page.component.html',
  styleUrls: ['./orders-page.component.css']
})

export class OrdersPageComponent {
  orders!: Order[];
  
  constructor(activatedRoute:ActivatedRoute, orderService:OrderService) {
    //ogni volta che 'params' cambia, chiama la funzione dentro 'subscribe()'
    activatedRoute.params.subscribe((params) => {
      orderService.getAllOrders(params.userToken).subscribe((serverOrders) => {
        this.orders = serverOrders; //riceve tutti gli ordini effettuati da un utente
      });
    });
  }
}

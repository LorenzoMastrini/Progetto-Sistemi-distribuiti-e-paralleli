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
  
  constructor(activatedRoute:ActivatedRoute, filmService:FilmService, private userService:UserService, private orderService:OrderService) {
    let ordersObservable: Observable<Order[]>; //per ottere gli observable di tutti i metodi chiamati che si connettono al backend, poi facendo subscribe per ottere i film
    //altrimenti dovrei fare subscribe per ognuno dei metodi chiamati separatamente
    console.log(this.userService.currentUser.id);

    //ogni volta che 'params' cambia, chiama la funzione dentro 'subscribe()'
    activatedRoute.params.subscribe((params) => {
      orderService.getAllOrders(params.userId).subscribe((serverOrders) => {
        this.orders = serverOrders;
      }); //se non è stato cercato nulla mostra tutto per default

      ordersObservable.subscribe((serverOrders) => {
        this.orders = serverOrders;
        console.log(serverOrders);
      });
    });
  }
}

import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { AdminService } from 'src/app/services/admin.service';
import { Order } from 'src/app/shared/models/Order';

@Component({
  selector: 'app-admin-orders',
  templateUrl: './admin-orders.component.html',
  styleUrls: ['./admin-orders.component.css']
})

export class AdminOrdersComponent {
  orders!: Order[];

  constructor(activatedRoute: ActivatedRoute,
              adminService:AdminService) {
    let ordersObservable: Observable<Order[]>; //per ottere gli observable di tutti i metodi chiamati che si connettono al backend, poi facendo subscribe per ottere i film
    //altrimenti dovrei fare subscribe per ognuno dei metodi chiamati separatamente
    
    //ogni volta che 'params' cambia, chiama la funzione dentro 'subscribe()'
    activatedRoute.params.subscribe(() => {
      ordersObservable = adminService.getAllOrders(); //se non è stato cercato nulla mostra tutto per default

      ordersObservable.subscribe((serverOrders) => {
        this.orders = serverOrders;
      });
    });
  }
}
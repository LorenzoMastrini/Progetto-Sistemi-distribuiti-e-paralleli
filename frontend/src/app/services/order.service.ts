import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { BOOK_TICKETS_URL, USER_ORDERS_URL } from '../shared/constants/urls';
import { Order } from '../shared/models/Order';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class OrderService {
  private order: Order = this.getOrderFromLocalStorage();
  private orderSubject: BehaviorSubject<Order> = new BehaviorSubject(this.order);
  
  constructor(private http:HttpClient) { }
  
  getOrderObservable(): Observable<Order> {
    return this.orderSubject.asObservable();
  }

  createOrder(order: Order): void {
    this.order = order;
    this.setOrderToLocalStorage();
  }

  private setOrderToLocalStorage(): void {
    const orderJson = JSON.stringify(this.order);
    localStorage.setItem('Order', orderJson);
    this.orderSubject.next(this.order);
  }

  private getOrderFromLocalStorage(): Order {
    const orderJson = localStorage.getItem('Order');
    return orderJson ? JSON.parse(orderJson): new Order();
  }

  reserve(): Observable<Order> {
    console.log(this.order);
    return this.http.post<Order>(BOOK_TICKETS_URL, this.order);
  }

  getAllOrders(userId: string): Observable<Order[]> {
    return this.http.get<Order[]>(USER_ORDERS_URL + userId);
  }
}
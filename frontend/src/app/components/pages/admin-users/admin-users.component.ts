import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs';
import { AdminService } from 'src/app/services/admin.service';
import { User } from 'src/app/shared/models/User';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.css']
})

export class AdminUsersComponent {
  users!: User[];

  constructor(activatedRoute: ActivatedRoute, private adminService:AdminService) {
    let usersObservable: Observable<User[]>; //per ottere gli observable di tutti i metodi chiamati che si connettono al backend, poi facendo subscribe per ottere i film
    //altrimenti dovrei fare subscribe per ognuno dei metodi chiamati separatamente
    
    //ogni volta che 'params' cambia, chiama la funzione dentro 'subscribe()'
    activatedRoute.params.subscribe(() => {
      usersObservable = adminService.getAllUsers(); //se non è stato cercato nulla mostra tutto per default

      usersObservable.subscribe((serverUsers) => {
        this.users = serverUsers;
      });
    });
  }

  changeAdminStatus(userId: string) {
    this.adminService.changeAdminStatus(userId).subscribe(() => {
      window.location.reload();
    });
  }
}
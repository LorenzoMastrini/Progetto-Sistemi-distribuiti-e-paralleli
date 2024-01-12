import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { User } from '../shared/models/User';
import { IUserLogin } from '../shared/interfaces/IUserLogin';
import { HttpClient } from '@angular/common/http';
import { USER_LOGIN_URL, USER_REGISTER_URL } from '../shared/constants/urls';
import { ToastrService } from 'ngx-toastr';
import { IUserRegister } from '../shared/interfaces/IUserRegister';
import { Router } from '@angular/router';


const USER_KEY = 'User'; //chiave per modificare l'utente salvato nel localStorage

@Injectable({
  providedIn: 'root'
})

export class UserService {
  private userSubject = new BehaviorSubject<User>(this.getUserFromLocalStorage()); //questo ha modalità di read e write
  //non voglio che le informazioni dell'utente siano modificabili da altri se non lo UserService, quindi creo l'Observable
  public userObservable: Observable<User>; //voglio esporre i dati dell'utente al di fuori di UserService

  constructor(private http:HttpClient,
              private toastrService:ToastrService,
              private router:Router) {
    this.userObservable = this.userSubject.asObservable(); //versione read only di userSubject, da esporre fuori dallo UserService
  }

  public get currentUser(): User {
    return this.userSubject.value; //ultimo valore dello userSubject
  }

  //uso localStorage per salvare l'utente così da non dover rifare il login dopo un refresh della pagina (come cart-page)
  private setUserToLocalStorage(user:User) {
    localStorage.setItem(USER_KEY, JSON.stringify(user)); //converto l'utente in JSON
  }

  private getUserFromLocalStorage(): User {
    const userJson = localStorage.getItem(USER_KEY);
    if(userJson) {
      return JSON.parse(userJson) as User;
    } else {
      return new User();
    }
  }

  login(userLogin:IUserLogin): Observable<User> {
    //non posso usare subscribe perché il tipo di ritorno sarebbe Subscription, non Observable
    //se non voglio cambiare ilvalore del risulato posso usare pipe(tap())
    return this.http.post<User>(USER_LOGIN_URL, userLogin).pipe(tap({
        next: (user) => { //risultato positivo
          this.setUserToLocalStorage(user); //salva l'utente dopo il login avvenuto con successo
          this.userSubject.next(user); //aggiorna lo userSubject con il nuovo utente
          this.toastrService.success(
            `Benvenuto/a al cinema ${user.name}!`,
            'Login completato'
          );
        },
        error: (errorResponse) => { //errore
          this.toastrService.error(errorResponse.error, 'Login fallito');
        }
      })
    );
  }
  
  logout() {
    this.userSubject.next(new User());
    localStorage.removeItem(USER_KEY);
    window.location.reload(); //refresh della pagina
    this.router.navigateByUrl('/');
  }

  register(userRegister:IUserRegister): Observable<User> {
    return this.http.post<User>(USER_REGISTER_URL, userRegister).pipe(tap({
      next: (user) => {
        this.setUserToLocalStorage(user);
        this.userSubject.next(user);
        this.toastrService.success(
          `Benvenuto/a al cinema ${user.name}!`,
          'Registrazione completata'
        )
      },
      error: (errorResponse) => {
        this.toastrService.error(errorResponse.error, 'Registrazione fallita');
      }
    }));
  }
}

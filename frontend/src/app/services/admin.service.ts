import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Schedule } from '../shared/models/Schedule';
import { HttpClient } from '@angular/common/http';
import { ADMIN_ADD_FILM, ADMIN_ADD_SCHEDULE, ADMIN_CHANGE_ADMIN_STATUS, ADMIN_GET_ALL_SCHEDULES, ADMIN_GET_ALL_USERS } from '../shared/constants/urls';
import { IAdminAddSchedule } from '../shared/interfaces/IAdminAddSchedule';
import { Film } from '../shared/models/Film';
import { IAdminAddFilm } from '../shared/interfaces/IAdminAddFilm';
import { User } from '../shared/models/User';

@Injectable({
  providedIn: 'root'
})

export class AdminService {
  constructor(private http:HttpClient) { }

  getAllSchedules(): Observable<Schedule[]> {
    return this.http.get<Schedule[]>(ADMIN_GET_ALL_SCHEDULES);
  }

  addSchedule(newSchedule:IAdminAddSchedule): Observable<Schedule> {
    return this.http.post<Schedule>(ADMIN_ADD_SCHEDULE, newSchedule);
  }

  addFilm(newFilm:IAdminAddFilm): Observable<Film> {
    return this.http.post<Film>(ADMIN_ADD_FILM, newFilm);
  }

  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(ADMIN_GET_ALL_USERS);
  }

  changeAdminStatus(userId: string): Observable<User> {
    return this.http.put<User>(ADMIN_CHANGE_ADMIN_STATUS + userId, []);
  }
}

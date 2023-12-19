import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Schedule } from '../shared/models/Schedule';
import { HttpClient } from '@angular/common/http';
import { ADMIN_ADD_FILM, ADMIN_ADD_SCHEDULE, ADMIN_GET_ALL_SCHEDULES } from '../shared/constants/urls';
import { IAdminAddSchedule } from '../shared/interfaces/IAdminAddSchedule';
import { Film } from '../shared/models/Film';
import { IAdminAddFilm } from '../shared/interfaces/IAdminAddFilm';

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
}

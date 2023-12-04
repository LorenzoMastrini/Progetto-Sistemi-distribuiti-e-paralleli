import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/pages/home/home.component';
import { FilmPageComponent } from './components/pages/film-page/film-page.component';
import { LoginPageComponent } from './components/pages/login-page/login-page.component';

const routes: Routes = [
  { path:"", component: HomeComponent }, //homepage dell'app
  //{ path:"search/:searchTerm", component: HomeComponent }, //forse utile con name al posto di searchTerm
  { path:"film/:name", component: FilmPageComponent },
  { path:"login", component: LoginPageComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }

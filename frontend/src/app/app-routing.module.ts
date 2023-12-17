import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/pages/home/home.component';
import { FilmPageComponent } from './components/pages/film-page/film-page.component';
import { LoginPageComponent } from './components/pages/login-page/login-page.component';
import { RegisterPageComponent } from './components/pages/register-page/register-page.component';
import { OrdersPageComponent } from './components/pages/orders-page/orders-page.component';
import { PaymentPageComponent } from './components/pages/payment-page/payment-page.component';
import { AdminHomeComponent } from './components/pages/admin-home/admin-home.component';
import { AdminAddFilmComponent } from './components/pages/admin-add-film/admin-add-film.component';

const routes: Routes = [
  { path:"", component: HomeComponent }, //homepage dell'app
  { path:"admin", component: AdminHomeComponent }, //homepage dell'app
  //{ path:"search/:searchTerm", component: HomeComponent }, //forse utile con name al posto di searchTerm
  { path:"film/:name", component: FilmPageComponent },
  { path:"login", component: LoginPageComponent },
  { path:"register", component: RegisterPageComponent },
  { path:"payment", component: PaymentPageComponent },
  { path:"users/orders/:userToken", component: OrdersPageComponent },
  { path:"admin/add-film", component: AdminAddFilmComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
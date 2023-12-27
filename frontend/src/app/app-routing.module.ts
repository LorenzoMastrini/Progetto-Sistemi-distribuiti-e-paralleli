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
import { AdminOrdersComponent } from './components/pages/admin-orders/admin-orders.component';
import { AdminUsersComponent } from './components/pages/admin-users/admin-users.component';
import { isAdminGuard } from './guards/is-admin.guard';
import { isAuthenticatedGuard } from './guards/is-authenticated.guard';

const routes: Routes = [
  { path:"", component: HomeComponent }, //homepage dell'app
  { path:"admin", component: AdminHomeComponent, canActivate: [isAdminGuard]}, //homepage dell'app per un utente admin
  { path:"film/:name", component: FilmPageComponent },
  { path:"login", component: LoginPageComponent },
  { path:"register", component: RegisterPageComponent },
  { path:"payment", component: PaymentPageComponent, canActivate: [isAuthenticatedGuard] },
  { path:"users/orders/:userToken", component: OrdersPageComponent, canActivate: [isAuthenticatedGuard] },
  { path:"admin/add-film", component: AdminAddFilmComponent, canActivate: [isAdminGuard] },
  { path:"admin/orders", component: AdminOrdersComponent, canActivate: [isAdminGuard] },
  { path:"admin/users", component: AdminUsersComponent, canActivate: [isAdminGuard] }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
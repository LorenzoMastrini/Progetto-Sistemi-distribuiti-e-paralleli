import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'; //per la connessione al backend
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/partials/header/header.component';
import { HomeComponent } from './components/pages/home/home.component';
import { FilmPageComponent } from './components/pages/film-page/film-page.component';
import { TitleComponent } from './components/partials/title/title.component';
import { NotFoundComponent } from './components/partials/not-found/not-found.component';
import { MatSliderModule } from '@angular/material/slider';
import { LoginPageComponent } from './components/pages/login-page/login-page.component';
import { ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { InputContainerComponent } from './components/partials/input-container/input-container.component';
import { InputValidationComponent } from './components/partials/input-validation/input-validation.component';
import { TextInputComponent } from './components/partials/text-input/text-input.component';
import { DefaultButtonComponent } from './components/partials/default-button/default-button.component';
import { RegisterPageComponent } from './components/pages/register-page/register-page.component';
import { OrdersPageComponent } from './components/pages/orders-page/orders-page.component';
import { PaymentPageComponent } from './components/pages/payment-page/payment-page.component';
import { AdminHomeComponent } from './components/pages/admin-home/admin-home.component';
import { AdminAddFilmComponent } from './components/pages/admin-add-film/admin-add-film.component';
import { AdminAddScheduleComponent } from './components/partials/admin-add-schedule/admin-add-schedule.component';
import { AdminOrdersComponent } from './components/pages/admin-orders/admin-orders.component';
import { AdminUsersComponent } from './components/pages/admin-users/admin-users.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HomeComponent,
    FilmPageComponent,
    TitleComponent,
    NotFoundComponent,
    LoginPageComponent,
    InputContainerComponent,
    InputValidationComponent,
    TextInputComponent,
    DefaultButtonComponent,
    RegisterPageComponent,
    OrdersPageComponent,
    PaymentPageComponent,
    AdminHomeComponent,
    AdminAddFilmComponent,
    AdminAddScheduleComponent,
    AdminOrdersComponent,
    AdminUsersComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    MatSliderModule,
    HttpClientModule,
    ReactiveFormsModule, //per usare loginForm dentro l'html
    ToastrModule.forRoot({ //configurazione parametri globali per questo progetto
      timeOut:3000, //i messaggi durano 3 secondi
      positionClass:'toast-bottom-right', //i messaggi compaiono in basso a destra
      newestOnTop:false //i nuovi messaggi compaiono dal basso e spingono verso l'alto i precedenti
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule { }

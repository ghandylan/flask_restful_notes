import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {FormComponent} from './components/form/form.component';
import {FormsModule} from "@angular/forms";
import {UsersComponent} from './components/users/users.component';
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {UpdateComponent} from './components/update/update.component';
import {LoginComponent} from './components/login/login.component';
import {RegisterComponent} from './components/register/register.component';
import {JwtInterceptor} from "../services/jwt-interceptor.service";
import { NotesComponent } from './components/notes/notes.component';

@NgModule({
  declarations: [
    AppComponent,
    FormComponent,
    UsersComponent,
    UpdateComponent,
    LoginComponent,
    RegisterComponent,
    NotesComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [{provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true}],
  bootstrap: [AppComponent]
})
export class AppModule {
}

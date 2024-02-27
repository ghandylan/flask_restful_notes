import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {FormComponent} from "./components/form/form.component";
import {UsersComponent} from "./components/users/users.component";
import {UpdateComponent} from "./components/update/update.component";
import {RegisterComponent} from "./components/register/register.component";
import {LoginComponent} from "./components/login/login.component";
import {AuthGuard} from "../auth/authguard.service";

const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'users', component: UsersComponent, canActivate: [AuthGuard]},
  {path: 'form', component: FormComponent, canActivate: [AuthGuard]},
  {path: 'update/:userId', component: UpdateComponent, canActivate: [AuthGuard]},
  {path: 'register', component: RegisterComponent},
  {path: 'login', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}

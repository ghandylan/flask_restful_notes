import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  constructor() { }

  public isLoggedIn(): boolean {
    return localStorage.getItem('access_token') !== null;
  }
}

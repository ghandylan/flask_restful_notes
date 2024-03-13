import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {catchError, Observable, throwError} from "rxjs";
import {User} from "../models/user";
import {Router} from "@angular/router";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:5000/';

  constructor(private http: HttpClient, private router: Router) {
  }

  loginUser(username: string, password: string): Observable<any> {
    const body = {username: username, password: password}
    return this.http.post(this.apiUrl + 'login', body);
  }

  logoutUser(): Observable<any> {
    // return this.http.post(this.apiUrl + 'logout', {}, {headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}});
    // get token from local storage
    const token = localStorage.getItem('access_token');
    // if response is status is 401, this means the token is invalid. log the user out
    const headers = {
      Authorization: 'Bearer ' + token
    };

    return this.http.post(this.apiUrl + 'logout', {}, {headers, observe: 'response'})
      .pipe(
        catchError((error: HttpErrorResponse) => {
          if (error.status === 401) {
            // Handle logout or token invalidation here
            console.log('Token is invalid');
            localStorage.removeItem('access_token');
            // Redirect the user to the login page
            this.router.navigate(['/login']);
          }
          return throwError(error);
        })
      );
  }


  registerUser(user: User): Observable<any> {
    return this.http.post(this.apiUrl + 'user', user);
  }


  getUserIdByUsername(username: string): Observable<any> {
    return this.http.get(this.apiUrl + 'user/' + username);

  }

  getUsers(): Observable<any> {
    return this.http.get(this.apiUrl + 'users');
  }


  deleteUser(userId: number): Observable<any> {
    return this.http.delete(this.apiUrl + 'user/' + userId);
  }

  updateUser(userId: number, newDetails: User): Observable<any> {
    return this.http.put(this.apiUrl + 'user/' + userId, newDetails);
  }
}

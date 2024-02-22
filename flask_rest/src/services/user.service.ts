import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {User} from "../models/user";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:5000/';

  constructor(private http: HttpClient) {
  }

  loginUser(username: string, password: string): Observable<any> {
    const body = {username: username, password: password}
    return this.http.post(this.apiUrl + 'login', body);
  }

  logoutUser(): Observable<any> {
    // return this.http.post(this.apiUrl + 'logout', {}, {headers: {Authorization: 'Bearer ' + localStorage.getItem('access_token')}});
    // get token from local storage
    const token = localStorage.getItem('access_token');
    return this.http.post(this.apiUrl + 'logout', {}, {headers: {Authorization: 'Bearer ' + token}});
  }

  getUser(userId: number): Observable<any> {
    return this.http.get(this.apiUrl + 'user/' + userId);
  }

  getUsers(): Observable<any> {
    return this.http.get(this.apiUrl + 'users');
  }

  addUser(user: User): Observable<any> {
    return this.http.post(this.apiUrl + 'user', user);
  }

  deleteUser(userId: number): Observable<any> {
    return this.http.delete(this.apiUrl + 'user/' + userId);
  }

  updateUser(userId: number, newDetails: User): Observable<any> {
    return this.http.put(this.apiUrl + 'user/' + userId, newDetails);
  }
}

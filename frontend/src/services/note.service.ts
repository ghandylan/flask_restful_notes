import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Note} from "../models/note";
import {Observable} from "rxjs";
import {UserService} from "./user.service";

@Injectable({
  providedIn: 'root'
})
export class NoteService {
  private apiUrl = 'http://localhost:5000/';
  private userService: UserService;

  constructor(private http: HttpClient, userService: UserService) {
    this.userService = userService;
  }

  showNotes(): Observable<Note[]> {
    // get jwt token from local storage
    const token = localStorage.getItem('access_token');

    // set the Authorization bearer token as the Jwt
    const headers = {
      Authorization: 'Bearer ' + token
    };

    // if token is not null
    if (token) {
      // decode the token
      // set the username to the decoded token's username
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      const username = decodedToken.sub.username;
    }
    return this.http.get<Note[]>(this.apiUrl + '/notes', {headers})
  }

  addNote(note: Note): Observable<any> {
    // get the jwt from local storage
    const token = localStorage.getItem('access_token');
    // get the claims from the jwt
    if (token) {
      const decodedToken = JSON.parse(atob(token.split('.')[1]));
      const username = decodedToken.sub.username;
      // get the user's id from the server
      this.userService.getUserIdByUsername(username).subscribe(
        (response: any) => {
          // set the note's user_id to the current user's id
          note.user_id = response.id;

        },
        (error) => {
          console.error(error);
        }
      );


    }
    // set the note's user_id to the current user's id
    return this.http.post(this.apiUrl + 'note', note);
  }

  deleteNoteById(id: number) : Observable<any> {
    console.log((this.apiUrl + 'note/' + id));

    // get jwt token from local storage
    const token = localStorage.getItem('access_token');

    // set the Authorization bearer token as the Jwt
    const headers = {
      Authorization: 'Bearer ' + token
    };

    return this.http.delete(this.apiUrl + 'note/' + id, {headers});
  }
}

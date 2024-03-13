import {Component, OnInit} from '@angular/core';
import {Note} from "../../../models/note";
import {NoteService} from "../../../services/note.service";
import {Router} from "@angular/router";
import {UserService} from "../../../services/user.service";

@Component({
  selector: 'app-notes',
  templateUrl: './notes.component.html',
  styleUrls: ['./notes.component.css']
})
export class NotesComponent implements OnInit {
  notes: Note[] = [];

  constructor(private noteService: NoteService, private router: Router, private userService: UserService) {
  }

  ngOnInit(): void {
    this.noteService.showNotes().subscribe(
      (notes: Note[]) => {
        this.notes = notes;
      },
      (error) => {
        console.error(error);
      }
    );
  }

  navigateToAddNote(): void {
    this.router.navigate(['/form']);
  }

  onLogout() {
    this.userService.logoutUser().subscribe(
      (response) => {
        console.log('User logged out:', response);
        localStorage.removeItem('access_token');
        this.router.navigate(['/login']);
      },
      (error) => {
        console.error('Error logging out:', error);
      }
    );
  }
}

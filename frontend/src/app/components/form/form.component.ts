import {Component} from '@angular/core';
import {NgForm} from "@angular/forms";
import {UserService} from "../../../services/user.service";
import {Router} from "@angular/router";
import {tap} from "rxjs/operators";
import {Note} from "../../../models/note";
import {NoteService} from "../../../services/note.service";

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent {
  // Initialize a new user object
  note: Note = {
    id: 0,
    title: '',
    content: '',
    user_id: 0
  };

  constructor(private noteService: NoteService, private userService: UserService, private router: Router) {
  }

  onSubmit(addForm: NgForm): void {
    // Check if the form is valid
    if (addForm.valid) {
      // Prepare the user data to be sent to the backend
      const newNote = this.note;

      // Use UserService to send the new user data to the backend
      this.noteService.addNote(newNote).pipe(
        tap(
          // Log the response on successful submission
          (response) => {
            console.log('Data successfully submitted:', response);
          },
          // Log the error on failed submission
          (error) => {
            console.error('Error submitting data:', error);
          }
        )
      ).subscribe();
    }
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

  navigateToUsers() {
    this.router.navigate(['/notes']);
  }
}

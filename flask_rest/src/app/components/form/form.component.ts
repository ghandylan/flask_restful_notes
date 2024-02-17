import {Component} from '@angular/core';
import {User} from "../../../models/user";
import {NgForm} from "@angular/forms";
import {UserService} from "../../../services/user.service";
import {Router} from "@angular/router";
import {tap} from "rxjs/operators";

@Component({
  selector: 'app-form',
  templateUrl: './form.component.html',
  styleUrls: ['./form.component.css']
})
export class FormComponent {
  // Initialize a new user object
  user: User = {
    id: 0,
    name: '',
    phone: ''
  };

  constructor(private userService: UserService, private router: Router) {
  }

  onSubmit(addForm: NgForm): void {
    // Check if the form is valid
    if (addForm.valid) {
      // Prepare the user data to be sent to the backend
      const newUser = this.user;

      // Use UserService to send the new user data to the backend
      this.userService.addUser(newUser).pipe(
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

  navigateToUsers() {
    this.router.navigate(['/users']);
  }
}

import {Component} from '@angular/core';
import {UserService} from "../../../services/user.service";
import {ActivatedRoute, Router} from "@angular/router";
import {User} from "../../../models/user";
import {NgForm} from "@angular/forms";

@Component({
  selector: 'app-update',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css']
})
export class UpdateComponent {
  // Initialize a new user object
  user: User = {
    id: 0,
    name: '',
    phone: ''
  };

  constructor(private userService: UserService, private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit() {
    const userId = this.route.snapshot.params['userId'];
    this.userService.getUser(userId).subscribe((user: User) => {
      this.user = user;
      console.log('User:', this.user);
    });
  }

  onSubmit(updateForm: NgForm): void {
    if (updateForm.valid) {
      this.userService.updateUser(this.user.id, this.user).subscribe(
        (response) => {
          console.log('User successfully updated:', response);
          this.router.navigate(['/users']);
        },
        (error) => {
          console.error('Error updating user:', error);
        }
      );
    }
  }

  navigateToUsers() {
    this.router.navigate(['/users']);
  }
}

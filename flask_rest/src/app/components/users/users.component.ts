import {Component} from '@angular/core';
import {User} from "../../../models/user";
import {UserService} from "../../../services/user.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent {
  users: User[] = [];

  constructor(private userService: UserService, private router: Router) {
  }

  ngOnInit() {
    this.userService.getUsers().subscribe((users: User[]) => {
      this.users = users;
    });
  }

  deleteUserOnClick(userId: number) {
    this.userService.deleteUser(userId).subscribe(
      // Log the response on successful submission
      (response) => {
        console.log('Data successfully deleted:', response);
        this.ngOnInit();
      },
      // Log the error on failed submission
      (error) => {
        console.error('Error deleting data:', error);
      })
  }

  navigateToUpdate(userId: number) {
    this.router.navigate(['/update/' + userId]);
  }

  navigateToForm() {
    this.router.navigate(['/form']);
  }
}
